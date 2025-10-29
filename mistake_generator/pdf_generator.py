"""
PDF生成模块
生成专业的错题卷PDF文档
"""
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


class PDFGenerator:
    """PDF生成器"""

    def __init__(self, output_dir: Path):
        """
        初始化PDF生成器

        Args:
            output_dir: PDF输出目录
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 注册中文字体（使用系统字体）
        self._register_fonts()

        # 创建样式
        self.styles = self._create_styles()

    def _register_fonts(self):
        """注册中文字体"""
        try:
            # 尝试注册常见的中文字体路径
            font_paths = [
                # Windows
                "C:/Windows/Fonts/simsun.ttc",
                "C:/Windows/Fonts/simhei.ttf",
                # Linux
                "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                # macOS
                "/System/Library/Fonts/PingFang.ttc",
                "/Library/Fonts/Arial Unicode.ttf",
            ]

            for font_path in font_paths:
                if Path(font_path).exists():
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        print(f"成功注册字体: {font_path}")
                        return
                    except:
                        continue

            # 如果都失败，使用默认字体（可能不支持中文）
            print("警告：未找到中文字体，PDF可能无法正确显示中文")

        except Exception as e:
            print(f"字体注册失败: {e}")

    def _create_styles(self):
        """创建文档样式"""
        styles = getSampleStyleSheet()

        # 标题样式
        styles.add(ParagraphStyle(
            name='ChineseTitle',
            fontName='ChineseFont',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=colors.HexColor('#333333')
        ))

        # 子标题样式
        styles.add(ParagraphStyle(
            name='ChineseHeading',
            fontName='ChineseFont',
            fontSize=14,
            leading=18,
            spaceAfter=10,
            textColor=colors.HexColor('#1a73e8')
        ))

        # 正文样式
        styles.add(ParagraphStyle(
            name='ChineseBody',
            fontName='ChineseFont',
            fontSize=11,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=8
        ))

        # 题号样式
        styles.add(ParagraphStyle(
            name='QuestionNumber',
            fontName='ChineseFont',
            fontSize=11,
            leading=16,
            textColor=colors.HexColor('#c62828'),
            spaceAfter=4
        ))

        return styles

    def generate_mistake_paper(
        self,
        practice_set: Dict[str, List[Dict[str, Any]]],
        output_filename: str = None,
        include_answers: bool = False
    ) -> Path:
        """
        生成错题卷PDF

        Args:
            practice_set: 练习题集（按题型分类）
            output_filename: 输出文件名，如果不指定则自动生成
            include_answers: 是否包含答案页

        Returns:
            生成的PDF文件路径
        """
        # 生成文件名
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"错题练习_{timestamp}.pdf"

        output_path = self.output_dir / output_filename

        print(f"\n正在生成PDF: {output_filename}...")

        # 创建PDF文档
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )

        # 构建文档内容
        story = []

        # 添加标题
        title = Paragraph("错题练习卷", self.styles['ChineseTitle'])
        story.append(title)
        story.append(Spacer(1, 10*mm))

        # 添加说明
        info_text = f"""
        <para align=center>
        生成时间：{datetime.now().strftime("%Y年%m月%d日")} &nbsp;&nbsp;
        姓名：__________ &nbsp;&nbsp;
        用时：____分钟
        </para>
        """
        info = Paragraph(info_text, self.styles['ChineseBody'])
        story.append(info)
        story.append(Spacer(1, 8*mm))

        # 按题型添加题目
        question_counter = 1
        all_answers = []  # 保存所有答案（如果需要答案页）

        for q_type, sections in practice_set.items():
            if not sections:
                continue

            # 题型标题
            type_title = Paragraph(f"<b>{q_type}</b>", self.styles['ChineseHeading'])
            story.append(type_title)
            story.append(Spacer(1, 4*mm))

            # 添加该题型下的所有题目
            for section in sections:
                section_items = []

                # 原题（如果包含）
                if section.get("original_question"):
                    original = section["original_question"]
                    q_text = self._format_question(
                        question_counter,
                        original["question_content"],
                        is_original=True
                    )
                    section_items.append(Paragraph(q_text, self.styles['ChineseBody']))
                    section_items.append(Spacer(1, 10*mm))  # 答题空间

                    # 保存答案
                    if include_answers and original.get("correct_answer"):
                        all_answers.append({
                            "number": question_counter,
                            "answer": original["correct_answer"],
                            "type": q_type
                        })

                    question_counter += 1

                # 相似题
                for similar_q in section.get("similar_questions", []):
                    q_text = self._format_question(
                        question_counter,
                        similar_q["question_content"]
                    )
                    section_items.append(Paragraph(q_text, self.styles['ChineseBody']))
                    section_items.append(Spacer(1, 10*mm))  # 答题空间

                    # 保存答案
                    if include_answers and similar_q.get("correct_answer"):
                        all_answers.append({
                            "number": question_counter,
                            "answer": similar_q["correct_answer"],
                            "type": q_type
                        })

                    question_counter += 1

                # 将该section的题目作为一组
                if section_items:
                    story.extend(section_items)
                    story.append(Spacer(1, 5*mm))

            # 每个题型后添加一些空间
            story.append(Spacer(1, 5*mm))

        # 添加答案页（如果需要）
        if include_answers and all_answers:
            story.append(PageBreak())
            story.append(Paragraph("参考答案", self.styles['ChineseTitle']))
            story.append(Spacer(1, 5*mm))

            current_type = None
            for ans in all_answers:
                if ans["type"] != current_type:
                    current_type = ans["type"]
                    story.append(Paragraph(f"<b>{current_type}</b>", self.styles['ChineseHeading']))
                    story.append(Spacer(1, 2*mm))

                answer_text = f"{ans['number']}. {ans['answer']}"
                story.append(Paragraph(answer_text, self.styles['ChineseBody']))

        # 生成PDF
        doc.build(story)

        print(f"PDF生成成功: {output_path}")
        print(f"  共 {question_counter - 1} 道题目")

        return output_path

    def _format_question(
        self,
        number: int,
        content: str,
        is_original: bool = False
    ) -> str:
        """
        格式化题目文本

        Args:
            number: 题号
            content: 题目内容
            is_original: 是否是原题

        Returns:
            格式化后的HTML文本
        """
        # 如果是原题，添加标记
        marker = " <font color='#c62828'>[原题]</font>" if is_original else ""

        # 格式化题号和内容
        formatted = f"<b>{number}.</b> {content}{marker}"

        return formatted


if __name__ == "__main__":
    # 测试代码
    from .config import MISTAKE_PAPERS_DIR, QUESTION_BANK_PATH
    from .question_bank import QuestionBank
    from .question_generator import QuestionGenerator

    # 加载题库
    bank = QuestionBank(QUESTION_BANK_PATH)
    mistakes = bank.get_mistakes()

    if not mistakes:
        print("题库中没有错题，无法生成PDF")
    else:
        # 生成练习题集
        generator = QuestionGenerator()
        practice_set = generator.generate_practice_set(mistakes[:3], similar_count=2)

        # 生成PDF
        pdf_gen = PDFGenerator(MISTAKE_PAPERS_DIR)
        pdf_path = pdf_gen.generate_mistake_paper(
            practice_set,
            include_answers=True
        )

        print(f"\nPDF已生成: {pdf_path}")
