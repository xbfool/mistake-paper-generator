#!/usr/bin/env python3
"""
小学数学计算题生成器 - LaTeX 版本
使用 xlop 包生成专业的竖式计算格式
"""
import sys
import io
import click
from pathlib import Path
from datetime import datetime

# 设置编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from math_generator.question_types import (
    OralQuestionGenerator,
    VerticalQuestionGenerator,
    FillBlankGenerator,
    ListVerticalGenerator
)
from math_generator.latex_generator import LaTeXGenerator


@click.command()
@click.option('--output', '-o', type=click.Path(), help='输出PDF文件路径')
@click.option('--count', type=int, default=30, help='总题目数量 [默认: 30]')
@click.option('--difficulty', type=click.Choice(['easy', 'medium', 'hard']),
              help='难度预设')
@click.option('--add', 'add_digits', help='加法位数组合')
@click.option('--sub', 'sub_digits', help='减法位数组合')
@click.option('--mul', 'mul_digits', help='乘法位数组合')
@click.option('--div', 'div_digits', help='除法位数组合')
@click.option('--oral', type=int, default=10, help='口算题数量')
@click.option('--vertical', type=int, default=10, help='竖式数量')
@click.option('--fill', type=int, default=5, help='填空题数量')
@click.option('--list', 'list_vertical', type=int, default=5, help='列竖式数量')
@click.option('--title', default='数学计算练习', help='试卷标题')
@click.option('--no-answers', is_flag=True, help='不生成答案页')
def main(output, count, difficulty, add_digits, sub_digits, mul_digits, div_digits,
         oral, vertical, fill, list_vertical, title, no_answers):
    """
    小学数学计算题生成器 - LaTeX 专业版

    \b
    使用 xlop 包生成标准的竖式计算格式

    基础用法:
      python generate_latex.py
      python generate_latex.py --difficulty medium
      python generate_latex.py --output 三年级练习.pdf
    """
    try:
        click.echo("\n使用 LaTeX 生成专业格式的数学练习题...\n")

        # 确定输出路径
        if not output:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = Path(f"output/math_latex_{timestamp}.pdf")
        else:
            output_path = Path(output)

        # 解析位数配置
        digit_configs = _parse_digit_configs(difficulty, add_digits, sub_digits, mul_digits, div_digits)

        # 生成题目
        click.echo("生成题目...")
        oral_gen = OralQuestionGenerator()
        vertical_gen = VerticalQuestionGenerator()
        fill_gen = FillBlankGenerator()
        list_gen = ListVerticalGenerator()

        oral_questions = oral_gen.generate_batch(oral, digit_configs=digit_configs) if oral > 0 else []
        vertical_questions = vertical_gen.generate_batch(vertical, digit_configs=digit_configs) if vertical > 0 else []
        fill_questions = fill_gen.generate_batch(fill, digit_configs=digit_configs) if fill > 0 else []
        list_questions = list_gen.generate_batch(list_vertical, digit_configs=digit_configs) if list_vertical > 0 else []

        total = len(oral_questions) + len(vertical_questions) + len(fill_questions) + len(list_questions)
        click.echo(f"共生成 {total} 道题目")

        # 使用 LaTeX 生成 PDF
        click.echo("\n使用 LaTeX 编译 PDF...")
        latex_gen = LaTeXGenerator()

        latex_gen.generate_pdf(
            output_path=output_path,
            title=title,
            oral_questions=oral_questions,
            vertical_questions=vertical_questions,
            fill_questions=fill_questions,
            list_vertical_questions=list_questions,
            include_answers=not no_answers
        )

        click.echo(f"\n✓ 成功生成: {output_path}")
        click.echo("\n提示：使用 LaTeX 生成的 PDF 格式专业，竖式标准！")

    except Exception as e:
        click.echo(f"\nERROR: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _parse_digit_configs(difficulty, add_digits, sub_digits, mul_digits, div_digits):
    """解析位数配置"""
    if difficulty:
        presets = {
            'easy': {
                'add': ['2x2', '2x1'],
                'sub': ['2x2', '2x1'],
                'mul': ['2x1', '1x1'],
                'div': ['2x1']
            },
            'medium': {
                'add': ['3x3', '3x2'],
                'sub': ['3x3', '3x2'],
                'mul': ['2x2', '3x1'],
                'div': ['3x1', '2x1']
            },
            'hard': {
                'add': ['4x4', '4x3'],
                'sub': ['4x4', '4x3'],
                'mul': ['3x2', '4x1'],
                'div': ['4x2', '4x1']
            }
        }
        return presets[difficulty]

    config = {}
    config['add'] = add_digits.split(',') if add_digits else ['3x3', '3x2']
    config['sub'] = sub_digits.split(',') if sub_digits else ['3x3', '3x2']
    config['mul'] = mul_digits.split(',') if mul_digits else ['2x2', '3x1']
    config['div'] = div_digits.split(',') if div_digits else ['3x1', '2x1']

    return config


if __name__ == '__main__':
    main()
