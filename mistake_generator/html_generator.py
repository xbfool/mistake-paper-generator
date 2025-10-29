"""
HTML生成模块
生成HTML格式的错题卷（可在浏览器中打开并打印为PDF）
"""
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime


class HTMLGenerator:
    """HTML生成器"""

    def __init__(self, output_dir: Path):
        """
        初始化HTML生成器

        Args:
            output_dir: HTML输出目录
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_mistake_paper(
        self,
        practice_set: Dict[str, List[Dict[str, Any]]],
        output_filename: str = None,
        include_answers: bool = False
    ) -> Path:
        """
        生成错题卷HTML

        Args:
            practice_set: 练习题集（按题型分类）
            output_filename: 输出文件名
            include_answers: 是否包含答案页

        Returns:
            生成的HTML文件路径
        """
        # 生成文件名
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"错题练习_{timestamp}.html"

        if not output_filename.endswith('.html'):
            output_filename = output_filename.replace('.pdf', '.html')

        output_path = self.output_dir / output_filename

        print(f"\n正在生成HTML: {output_filename}...", flush=True)

        # 构建HTML内容
        html_parts = []

        # HTML头部
        html_parts.append(self._generate_header())

        # 标题和信息
        html_parts.append(f"""
    <div class="header">
        <h1>错题练习卷</h1>
        <div class="info">
            <span>生成时间：{datetime.now().strftime("%Y年%m月%d日")}</span>
            <span>姓名：__________</span>
            <span>用时：____分钟</span>
        </div>
    </div>
    <hr class="divider">
""")

        # 按题型添加题目
        question_counter = 1
        all_answers = []

        for q_type, sections in practice_set.items():
            if not sections:
                continue

            html_parts.append(f'    <div class="question-type">\n')
            html_parts.append(f'        <h2>{q_type}</h2>\n')

            for section in sections:
                # 原题
                if section.get("original_question"):
                    original = section["original_question"]
                    html_parts.append(f'        <div class="question">\n')
                    html_parts.append(f'            <div class="question-number">{question_counter}. <span class="original-tag">[原题]</span></div>\n')
                    html_parts.append(f'            <div class="question-content">{self._escape_html(original["question_content"])}</div>\n')
                    html_parts.append(f'            <div class="answer-area"></div>\n')
                    html_parts.append(f'        </div>\n')

                    if include_answers and original.get("correct_answer"):
                        all_answers.append({
                            "number": question_counter,
                            "answer": original["correct_answer"],
                            "type": q_type
                        })

                    question_counter += 1

                # 相似题
                for similar_q in section.get("similar_questions", []):
                    html_parts.append(f'        <div class="question">\n')
                    html_parts.append(f'            <div class="question-number">{question_counter}.</div>\n')
                    html_parts.append(f'            <div class="question-content">{self._escape_html(similar_q["question_content"])}</div>\n')
                    html_parts.append(f'            <div class="answer-area"></div>\n')
                    html_parts.append(f'        </div>\n')

                    if include_answers and similar_q.get("correct_answer"):
                        all_answers.append({
                            "number": question_counter,
                            "answer": similar_q["correct_answer"],
                            "type": q_type
                        })

                    question_counter += 1

            html_parts.append(f'    </div>\n')

        # 答案页
        if include_answers and all_answers:
            html_parts.append(f'    <div class="page-break"></div>\n')
            html_parts.append(f'    <div class="answers-section">\n')
            html_parts.append(f'        <h1>参考答案</h1>\n')
            html_parts.append(f'        <hr class="divider">\n')

            current_type = None
            for ans in all_answers:
                if ans["type"] != current_type:
                    if current_type is not None:
                        html_parts.append(f'        </div>\n')
                    current_type = ans["type"]
                    html_parts.append(f'        <div class="answer-type">\n')
                    html_parts.append(f'            <h2>{current_type}</h2>\n')

                html_parts.append(f'            <div class="answer-item">\n')
                html_parts.append(f'                <span class="answer-number">{ans["number"]}.</span>\n')
                html_parts.append(f'                <span class="answer-content">{self._escape_html(ans["answer"])}</span>\n')
                html_parts.append(f'            </div>\n')

            if current_type is not None:
                html_parts.append(f'        </div>\n')

            html_parts.append(f'    </div>\n')

        # HTML尾部
        html_parts.append(self._generate_footer())

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_parts))

        print(f"HTML生成成功: {output_path}", flush=True)
        print(f"  共 {question_counter - 1} 道题目", flush=True)
        print(f"\n提示：", flush=True)
        print(f"  1. 在浏览器中打开该文件", flush=True)
        print(f"  2. 使用浏览器的打印功能（Ctrl+P）保存为PDF", flush=True)

        return output_path

    def _escape_html(self, text: str) -> str:
        """转义HTML特殊字符"""
        if not text:
            return ""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    def _generate_header(self) -> str:
        """生成HTML头部"""
        return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>错题练习卷</title>
    <style>
        @media print {
            .page-break {
                page-break-before: always;
            }
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: "Microsoft YaHei", "SimSun", "Arial", sans-serif;
            line-height: 1.6;
            padding: 20mm;
            max-width: 210mm;
            margin: 0 auto;
            background: white;
        }

        .header {
            text-align: center;
            margin-bottom: 20px;
        }

        h1 {
            font-size: 24px;
            margin-bottom: 15px;
            color: #333;
        }

        .info {
            font-size: 14px;
            color: #666;
        }

        .info span {
            margin: 0 15px;
        }

        .divider {
            border: none;
            border-top: 2px solid #333;
            margin: 20px 0;
        }

        .question-type {
            margin-bottom: 30px;
        }

        .question-type h2 {
            font-size: 16px;
            color: #1a73e8;
            margin-bottom: 15px;
            padding-bottom: 5px;
            border-bottom: 1px solid #ddd;
        }

        .question {
            margin-bottom: 25px;
            padding: 10px 0;
        }

        .question-number {
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }

        .original-tag {
            color: #c62828;
            font-size: 12px;
            font-weight: normal;
        }

        .question-content {
            margin-left: 20px;
            margin-bottom: 10px;
            line-height: 1.8;
        }

        .answer-area {
            margin-left: 20px;
            min-height: 60px;
            border-bottom: 1px dotted #ccc;
        }

        .answers-section {
            margin-top: 30px;
        }

        .answer-type {
            margin-bottom: 20px;
        }

        .answer-item {
            margin: 8px 0;
            padding-left: 20px;
        }

        .answer-number {
            font-weight: bold;
            color: #1a73e8;
            display: inline-block;
            min-width: 40px;
        }

        .answer-content {
            color: #333;
        }
    </style>
</head>
<body>
"""

    def _generate_footer(self) -> str:
        """生成HTML尾部"""
        return """</body>
</html>"""


if __name__ == "__main__":
    # 测试代码
    from .config import MISTAKE_PAPERS_DIR, QUESTION_BANK_PATH
    from .question_bank import QuestionBank
    from .question_generator import QuestionGenerator

    bank = QuestionBank(QUESTION_BANK_PATH)
    mistakes = bank.get_mistakes()

    if mistakes:
        generator = QuestionGenerator()
        practice_set = generator.generate_practice_set(mistakes[:3], similar_count=2)

        html_gen = HTMLGenerator(MISTAKE_PAPERS_DIR)
        html_path = html_gen.generate_mistake_paper(
            practice_set,
            include_answers=True
        )

        print(f"\nHTML已生成: {html_path}")
