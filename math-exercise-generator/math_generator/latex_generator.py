"""
LaTeX 生成器
使用 Jinja2 模板生成 LaTeX 代码，然后编译成 PDF
"""
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from jinja2 import Environment


class LaTeXGenerator:
    """LaTeX 生成器"""

    def __init__(self):
        """初始化 LaTeX 生成器"""
        self.template_dir = Path(__file__).parent.parent / "templates"

    def generate_pdf(self,
                    output_path: Path,
                    title: str,
                    oral_questions: List[Any],
                    vertical_questions: List[Any],
                    fill_questions: List[Any],
                    list_vertical_questions: List[Any],
                    include_answers: bool = True) -> None:
        """
        生成 PDF

        Args:
            output_path: 输出 PDF 路径
            title: 标题
            oral_questions: 口算题列表
            vertical_questions: 竖式题列表
            fill_questions: 填空题列表
            list_vertical_questions: 列竖式题列表
            include_answers: 是否包含答案
        """
        # 确保输出目录存在
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # 生成 .tex 文件
        tex_path = output_path.with_suffix('.tex')
        self._generate_tex(
            tex_path,
            title,
            oral_questions,
            vertical_questions,
            fill_questions,
            list_vertical_questions,
            include_answers
        )

        # 编译 PDF
        self._compile_pdf(tex_path, output_path)

    def _generate_tex(self,
                     tex_path: Path,
                     title: str,
                     oral_questions: List,
                     vertical_questions: List,
                     fill_questions: List,
                     list_vertical_questions: List,
                     include_answers: bool) -> None:
        """生成 .tex 文件"""

        # 读取模板
        template_path = self.template_dir / "worksheet_template.tex"
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()

        # 配置 Jinja2 环境，使用特殊分隔符避免与 LaTeX 冲突
        env = Environment(
            block_start_string='\\BLOCK{',
            block_end_string='}',
            variable_start_string='\\VAR{',
            variable_end_string='}',
            comment_start_string='\\#{',
            comment_end_string='}',
            line_statement_prefix='%%',
            line_comment_prefix='%#',
            trim_blocks=True,
            autoescape=False,
        )

        # 渲染模板
        template = env.from_string(template_content)

        tex_content = template.render(
            title=title,
            oral_questions=oral_questions,
            vertical_questions=vertical_questions,
            fill_questions=fill_questions,
            list_vertical_questions=list_vertical_questions,
            oral_points=3,
            vertical_points=5,
            fill_points=4,
            list_points=5,
            include_answers=include_answers
        )

        # 写入 .tex 文件
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(tex_content)

    def _compile_pdf(self, tex_path: Path, output_path: Path) -> None:
        """
        编译 LaTeX 为 PDF

        Args:
            tex_path: .tex 文件路径
            output_path: 输出 PDF 路径
        """
        # 在 .tex 文件所在目录编译
        work_dir = tex_path.parent

        # pdflatex 路径
        pdflatex_paths = [
            r'C:\Users\xbfoo\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe',
            r'C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe',
            'pdflatex'  # 如果在 PATH 中
        ]

        # 找到可用的 pdflatex
        pdflatex_cmd = None
        for path in pdflatex_paths:
            try:
                test_result = subprocess.run(
                    [path, '--version'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if test_result.returncode == 0:
                    pdflatex_cmd = path
                    break
            except (FileNotFoundError, subprocess.TimeoutExpired):
                continue

        if not pdflatex_cmd:
            raise RuntimeError("找不到 pdflatex 命令，请确保已安装 MiKTeX")

        # 调用 pdflatex（编译两次以确保引用正确）
        for i in range(2):
            result = subprocess.run(
                [pdflatex_cmd, '-interaction=nonstopmode', str(tex_path.name)],
                cwd=work_dir,
                capture_output=True,
                encoding='utf-8',
                errors='ignore'  # 忽略编码错误
            )

            if result.returncode != 0:
                raise RuntimeError(f"LaTeX 编译失败:\n{result.stdout}\n{result.stderr}")

        # 移动生成的 PDF 到目标位置
        generated_pdf = tex_path.with_suffix('.pdf')
        if generated_pdf.exists():
            if generated_pdf != output_path:
                generated_pdf.rename(output_path)

        # 清理临时文件
        self._cleanup_temp_files(tex_path)

    def _cleanup_temp_files(self, tex_path: Path) -> None:
        """清理 LaTeX 编译产生的临时文件"""
        temp_extensions = ['.aux', '.log', '.out']
        for ext in temp_extensions:
            temp_file = tex_path.with_suffix(ext)
            if temp_file.exists():
                temp_file.unlink()
