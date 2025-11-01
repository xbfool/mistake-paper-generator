"""
PDF 构建器
"""
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from .fonts import FontManager


class PDFBuilder:
    """PDF 构建器"""

    def __init__(self):
        """初始化 PDF 构建器"""
        # 初始化字体
        FontManager.initialize()
        self.font_name = FontManager.get_font_name()

        # A4 页面尺寸
        self.page_width, self.page_height = A4

        # 页边距
        self.margin_left = 20 * mm
        self.margin_right = 20 * mm
        self.margin_top = 20 * mm
        self.margin_bottom = 20 * mm

        # 可用区域
        self.content_width = self.page_width - self.margin_left - self.margin_right
        self.content_height = self.page_height - self.margin_top - self.margin_bottom

    def build(self,
             output_path: Path,
             title: str,
             oral_questions: List[Any],
             vertical_questions: List[Any],
             fill_questions: List[Any],
             list_vertical_questions: List[Any],
             include_answers: bool = True,
             answer_detailed: bool = False) -> None:
        """
        构建完整的 PDF

        Args:
            output_path: 输出文件路径
            title: 试卷标题
            oral_questions: 口算题列表
            vertical_questions: 竖式题列表
            fill_questions: 填空题列表
            list_vertical_questions: 列竖式题列表
            include_answers: 是否包含答案页
            answer_detailed: 答案是否包含详细步骤
        """
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 创建 PDF 画布
        c = canvas.Canvas(str(output_path), pagesize=A4)

        # 生成题目页
        self._draw_question_page(
            c,
            title,
            oral_questions,
            vertical_questions,
            fill_questions,
            list_vertical_questions
        )

        # 生成答案页
        if include_answers:
            c.showPage()  # 新页面
            self._draw_answer_page(
                c,
                oral_questions,
                vertical_questions,
                fill_questions,
                list_vertical_questions,
                detailed=answer_detailed
            )

        # 保存 PDF
        c.save()

    def _draw_question_page(self,
                           c: canvas.Canvas,
                           title: str,
                           oral_q: List,
                           vertical_q: List,
                           fill_q: List,
                           list_q: List) -> None:
        """绘制题目页"""
        y = self.page_height - self.margin_top

        # 标题
        y = self._draw_header(c, title, y)

        # 一、口算题
        if oral_q:
            y = self._draw_section_title(c, "一、口算题", len(oral_q), 3, y)
            y = self._draw_oral_questions(c, oral_q, y)

        # 二、竖式计算
        if vertical_q:
            y = self._draw_section_title(c, "二、竖式计算", len(vertical_q), 5, y)
            y = self._draw_vertical_questions(c, vertical_q, y)

        # 三、填空题
        if fill_q:
            y = self._draw_section_title(c, "三、填空题", len(fill_q), 4, y)
            y = self._draw_fill_questions(c, fill_q, y)

        # 四、列竖式计算
        if list_q:
            y = self._draw_section_title(c, "四、列竖式计算", len(list_q), 5, y)
            y = self._draw_list_vertical_questions(c, list_q, y)

    def _draw_header(self, c: canvas.Canvas, title: str, y: float) -> float:
        """绘制页眉"""
        # 标题（蓝色）
        c.setFillColor(colors.HexColor('#1e88e5'))
        c.setFont(self.font_name, 18)
        c.drawCentredString(self.page_width / 2, y, title)

        y -= 30

        # 信息栏（黑色）
        c.setFillColor(colors.black)
        c.setFont(self.font_name, 10)
        date_str = datetime.now().strftime('%Y年%m月%d日')
        info_text = f"姓名:__________  班级:__________  日期:{date_str}  成绩:__________"
        c.drawString(self.margin_left, y, info_text)

        y -= 20

        # 分隔线（蓝色）
        c.setStrokeColor(colors.HexColor('#1e88e5'))
        c.setLineWidth(2)
        c.line(self.margin_left, y, self.page_width - self.margin_right, y)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)

        return y - 15

    def _draw_section_title(self, c: canvas.Canvas, title: str, count: int, points: int, y: float) -> float:
        """绘制章节标题"""
        # 章节标题（深蓝色背景）
        c.setFillColor(colors.HexColor('#e3f2fd'))
        c.rect(self.margin_left - 5, y - 5, self.content_width + 10, 20, fill=1, stroke=0)

        # 标题文字（深蓝色）
        c.setFillColor(colors.HexColor('#1565c0'))
        c.setFont(self.font_name, 12)
        total_points = count * points
        section_text = f"{title}（每题{points}分，共{total_points}分）"
        c.drawString(self.margin_left, y, section_text)

        # 恢复黑色
        c.setFillColor(colors.black)

        return y - 25

    def _draw_oral_questions(self, c: canvas.Canvas, questions: List, y: float) -> float:
        """绘制口算题（横式排列）"""
        c.setFont(self.font_name, 12)

        # 每行2道题
        col_width = self.content_width / 2
        row_height = 35  # 增加行间距

        for i, q in enumerate(questions):
            row = i // 2
            col = i % 2

            x = self.margin_left + col * col_width
            current_y = y - row * row_height

            # 题号和题目
            text = f"{i + 1}. {q.question}"
            c.drawString(x, current_y, text)

        # 计算需要的总高度
        total_rows = (len(questions) + 1) // 2
        return y - total_rows * row_height - 15

    def _draw_vertical_questions(self, c: canvas.Canvas, questions: List, y: float) -> float:
        """绘制竖式计算题"""
        c.setFont(self.font_name, 11)

        # 每行2道题
        col_width = self.content_width / 2
        question_height = 90  # 每道竖式题的高度（增加间距）

        for i, q in enumerate(questions):
            row = i // 2
            col = i % 2

            x = self.margin_left + col * col_width + 30
            current_y = y - row * question_height

            # 绘制边框（参考教材格式）
            box_width = 150
            box_height = 80
            c.setLineWidth(1)
            c.rect(x - 30, current_y - 65, box_width, box_height, stroke=1, fill=0)

            # 绘制题号（在边框内左上角）
            c.setFont(self.font_name, 10)
            c.drawString(x - 25, current_y, f"{i + 1}")

            # 绘制竖式
            self._draw_vertical_format(c, q, x, current_y - 10)

        # 计算总高度
        total_rows = (len(questions) + 1) // 2
        return y - total_rows * question_height - 10

    def _draw_vertical_format(self, c: canvas.Canvas, question, x: float, y: float) -> None:
        """绘制竖式格式"""
        op = question.operation

        if op in ['add', 'sub']:
            a, b = question.numbers[:2]
            symbol = '+' if op == 'add' else '-'

            # 将数字转换为带空格的格式（参考教材）
            a_str = str(a)
            b_str = str(b)

            # 对齐到相同长度
            max_len = max(len(a_str), len(b_str))
            a_str = a_str.zfill(max_len)
            b_str = b_str.zfill(max_len)

            # 添加空格分隔每个数字
            a_spaced = ' '.join(list(a_str))
            b_spaced = ' '.join(list(b_str))

            c.setFont(self.font_name, 14)  # 较大字体

            # 计算宽度
            char_width = 10  # 每个字符（包括空格）的宽度
            total_width = len(a_spaced) * char_width

            # 第一个数（右对齐）
            c.drawRightString(x + total_width, y, a_spaced)

            # 符号和第二个数
            c.drawString(x - 20, y - 24, symbol)
            c.drawRightString(x + total_width, y - 24, b_spaced)

            # 横线
            c.setLineWidth(1.5)
            c.line(x - 25, y - 30, x + total_width + 5, y - 30)
            c.setLineWidth(1)

            # 答案框
            c.setFont(self.font_name, 11)
            c.drawString(x + 10, y - 48, "(          )")

        elif op == 'mul':
            a, b = question.numbers[:2]

            # 将数字转换为带空格的格式
            a_str = str(a)
            b_str = str(b)

            # 对齐到相同长度
            max_len = max(len(a_str), len(b_str))
            a_str = a_str.zfill(max_len)
            b_str = b_str.zfill(max_len)

            # 添加空格
            a_spaced = ' '.join(list(a_str))
            b_spaced = ' '.join(list(b_str))

            c.setFont(self.font_name, 14)

            # 计算宽度
            char_width = 10
            total_width = len(a_spaced) * char_width

            # 第一个数
            c.drawRightString(x + total_width, y, a_spaced)

            # 符号和第二个数
            c.drawString(x - 20, y - 24, '×')
            c.drawRightString(x + total_width, y - 24, b_spaced)

            # 横线
            c.setLineWidth(1.5)
            c.line(x - 25, y - 30, x + total_width + 5, y - 30)
            c.setLineWidth(1)

            # 答案框
            c.setFont(self.font_name, 11)
            c.drawString(x + 10, y - 48, "(          )")

        elif op == 'div':
            dividend, divisor = question.numbers[:2]

            # 除法竖式（严格按照教材标准）
            divisor_str = str(divisor)
            dividend_str = str(dividend)

            c.setFont(self.font_name, 14)

            # 除数（左边）
            divisor_x = x - 10
            c.drawString(divisor_x, y - 2, divisor_str)

            # 计算竖线的x位置（在除数右边留一点间距）
            divisor_width = len(divisor_str) * 9
            vertical_line_x = divisor_x + divisor_width + 5

            # 被除数（每个数字之间加空格）
            dividend_with_spaces = ' '.join(list(dividend_str))
            dividend_x = vertical_line_x + 5
            c.drawString(dividend_x, y - 2, dividend_with_spaces)

            # 计算横线长度（覆盖被除数）
            dividend_width = len(dividend_with_spaces) * 8

            # 画横线（在被除数上方）
            horizontal_y = y + 16
            c.setLineWidth(1.5)
            c.line(vertical_line_x, horizontal_y,
                   dividend_x + dividend_width, horizontal_y)

            # 画竖线（从横线垂直向下，到被除数下方）
            c.line(vertical_line_x, y - 10,
                   vertical_line_x, horizontal_y)
            c.setLineWidth(1)

            # 商的答案框（在横线上方）
            c.setFont(self.font_name, 10)
            c.drawString(dividend_x, horizontal_y + 5, "(          )")

    def _draw_fill_questions(self, c: canvas.Canvas, questions: List, y: float) -> float:
        """绘制填空题"""
        c.setFont(self.font_name, 11)

        row_height = 25

        for i, q in enumerate(questions):
            current_y = y - i * row_height

            # 题号和题目
            text = f"{i + 1}. {q.question}"
            c.drawString(self.margin_left, current_y, text)

        return y - len(questions) * row_height - 15

    def _draw_list_vertical_questions(self, c: canvas.Canvas, questions: List, y: float) -> float:
        """绘制列竖式计算题"""
        c.setFont(self.font_name, 11)

        question_height = 70  # 每道题预留空间

        for i, q in enumerate(questions):
            current_y = y - i * question_height

            # 题号和题目
            text = f"{i + 1}. {q.question}"
            c.drawString(self.margin_left, current_y, text)

            # 提示文字
            hint = "（请在下方列竖式计算）"
            c.setFont(self.font_name, 9)
            c.drawString(self.margin_left + 200, current_y, hint)
            c.setFont(self.font_name, 11)

        return y - len(questions) * question_height - 10

    def _draw_answer_page(self,
                         c: canvas.Canvas,
                         oral_q: List,
                         vertical_q: List,
                         fill_q: List,
                         list_q: List,
                         detailed: bool = False) -> None:
        """绘制答案页"""
        y = self.page_height - self.margin_top

        # 标题（绿色）
        c.setFillColor(colors.HexColor('#43a047'))
        c.setFont(self.font_name, 18)
        c.drawCentredString(self.page_width / 2, y, "参考答案")
        y -= 30

        # 分隔线（绿色）
        c.setStrokeColor(colors.HexColor('#43a047'))
        c.setLineWidth(2)
        c.line(self.margin_left, y, self.page_width - self.margin_right, y)
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        c.setFillColor(colors.black)

        y -= 20

        # 一、口算题答案
        if oral_q:
            y = self._draw_answer_section(c, "一、口算题", oral_q, y)

        # 二、竖式计算答案
        if vertical_q:
            y = self._draw_answer_section(c, "二、竖式计算", vertical_q, y)

        # 三、填空题答案
        if fill_q:
            y = self._draw_answer_section(c, "三、填空题", fill_q, y)

        # 四、列竖式答案
        if list_q:
            y = self._draw_answer_section(c, "四、列竖式计算", list_q, y)

    def _draw_answer_section(self, c: canvas.Canvas, title: str, questions: List, y: float) -> float:
        """绘制答案章节"""
        # 章节标题（深绿色）
        c.setFillColor(colors.HexColor('#2e7d32'))
        c.setFont(self.font_name, 12)
        c.drawString(self.margin_left, y, title)
        y -= 20

        # 答案内容（黑色）
        c.setFillColor(colors.black)
        c.setFont(self.font_name, 10)

        # 每行显示5个答案
        answers_per_row = 5
        col_width = self.content_width / answers_per_row

        for i, q in enumerate(questions):
            row = i // answers_per_row
            col = i % answers_per_row

            x = self.margin_left + col * col_width
            current_y = y - row * 18

            # 答案文本
            answer_text = f"{i + 1}. {q.answer}"
            c.drawString(x, current_y, answer_text)

        # 计算总高度
        total_rows = (len(questions) + answers_per_row - 1) // answers_per_row
        return y - total_rows * 18 - 25
