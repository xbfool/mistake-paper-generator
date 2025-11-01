#!/usr/bin/env python3
"""
小学数学计算题生成器
支持 1-4 位数的加减乘除运算
"""
import sys
import io
import click
from pathlib import Path
from datetime import datetime

# 设置 stdout 编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from math_generator.question_types import (
    OralQuestionGenerator,
    VerticalQuestionGenerator,
    FillBlankGenerator,
    ListVerticalGenerator
)
from math_generator.pdf import PDFBuilder


@click.command()
@click.option('--help', '-h', 'show_help', is_flag=True, help='显示此帮助信息')
@click.option('--output', '-o', type=click.Path(), help='输出PDF文件路径')
@click.option('--count', type=int, default=30, help='总题目数量 [默认: 30]')
@click.option('--difficulty', type=click.Choice(['easy', 'medium', 'hard']),
              help='难度预设 [easy|medium|hard]')
@click.option('--add', 'add_digits', help='加法位数组合，如: "3x3,3x2"')
@click.option('--sub', 'sub_digits', help='减法位数组合，如: "3x3,3x2"')
@click.option('--mul', 'mul_digits', help='乘法位数组合，如: "2x2,3x1"')
@click.option('--div', 'div_digits', help='除法位数组合，如: "3x1,4x2"')
@click.option('--force-carry', is_flag=True, help='强制所有加法题都需要进位')
@click.option('--no-carry', is_flag=True, help='强制所有加法题都不进位')
@click.option('--force-borrow', is_flag=True, help='强制所有减法题都需要退位')
@click.option('--no-borrow', is_flag=True, help='强制所有减法题都不退位')
@click.option('--allow-remainder', is_flag=True, default=True, help='允许除法有余数 [默认: 是]')
@click.option('--no-remainder', is_flag=True, help='只生成整除的除法题')
@click.option('--force-remainder', is_flag=True, help='强制除法必须有余数')
@click.option('--oral', type=int, default=10, help='口算题数量 [默认: 10]')
@click.option('--vertical', type=int, default=10, help='竖式计算数量 [默认: 10]')
@click.option('--fill', type=int, default=5, help='填空题数量 [默认: 5]')
@click.option('--list', 'list_vertical', type=int, default=5, help='列竖式数量 [默认: 5]')
@click.option('--title', default='数学计算练习', help='试卷标题')
@click.option('--no-answers', is_flag=True, help='不生成答案页')
@click.option('--batch', type=int, help='批量生成份数')
@click.option('--prefix', default='数学练习', help='批量生成文件名前缀')
def main(show_help, output, count, difficulty, add_digits, sub_digits, mul_digits, div_digits,
         force_carry, no_carry, force_borrow, no_borrow,
         allow_remainder, no_remainder, force_remainder,
         oral, vertical, fill, list_vertical, title, no_answers, batch, prefix):
    """
    小学数学计算题生成器 - 支持1-4位数的加减乘除运算

    \b
    基础用法:
      python generate.py                           # 生成默认30题
      python generate.py --count 50                # 生成50题
      python generate.py --output 练习1.pdf        # 指定输出文件

    \b
    难度预设:
      python generate.py --difficulty easy         # 简单（1-2位数）
      python generate.py --difficulty medium       # 中等（2-3位数）
      python generate.py --difficulty hard         # 困难（3-4位数）

    \b
    自定义位数:
      python generate.py --add 3x3,4x2             # 3位+3位, 4位+2位
      python generate.py --mul 2x2,3x1             # 2位×2位, 3位×1位
      python generate.py --div 4x2 --no-remainder  # 4位÷2位整除

    \b
    题型控制:
      python generate.py --oral 20 --vertical 10   # 20道口算 + 10道竖式
      python generate.py --fill 15 --list 0        # 15道填空，不要列竖式

    \b
    批量生成:
      python generate.py --batch 5 --prefix "第一周练习"

    \b
    位数格式说明:
      "AxB" 表示 A位数 运算 B位数
      示例: 2x2=两位数+两位数, 3x1=三位数×一位数, 4x2=四位数÷两位数
      多个用逗号分隔: --add 2x2,3x2,3x3

    \b
    更多示例请查看 README.md
    """
    # 如果显式指定 --help，显示帮助后退出
    if show_help:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        ctx.exit()

    try:
        # 处理批量生成
        if batch:
            click.echo(f"\n批量生成 {batch} 份练习...\n")
            for i in range(1, batch + 1):
                batch_output = Path(f"output/{prefix}_第{i}期.pdf") if not output else Path(output)
                click.echo(f"正在生成第 {i} 份...")
                _generate_single_pdf(
                    output=batch_output,
                    count=count,
                    difficulty=difficulty,
                    add_digits=add_digits,
                    sub_digits=sub_digits,
                    mul_digits=mul_digits,
                    div_digits=div_digits,
                    oral_count=oral,
                    vertical_count=vertical,
                    fill_count=fill,
                    list_count=list_vertical,
                    title=f"{title}（第{i}期）",
                    include_answers=not no_answers
                )
            click.echo(f"\n成功生成 {batch} 份练习！")
        else:
            # 单份生成
            _generate_single_pdf(
                output=output,
                count=count,
                difficulty=difficulty,
                add_digits=add_digits,
                sub_digits=sub_digits,
                mul_digits=mul_digits,
                div_digits=div_digits,
                oral_count=oral,
                vertical_count=vertical,
                fill_count=fill,
                list_count=list_vertical,
                title=title,
                include_answers=not no_answers
            )

    except Exception as e:
        click.echo(f"\nERROR: {e}", err=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)


def _generate_single_pdf(output, count, difficulty, add_digits, sub_digits, mul_digits, div_digits,
                        oral_count, vertical_count, fill_count, list_count, title, include_answers):
    """生成单份PDF"""

    # 确定输出路径
    if not output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = Path(f"output/math_exercise_{timestamp}.pdf")
    else:
        output_path = Path(output)

    # 解析位数配置
    digit_configs = _parse_digit_configs(difficulty, add_digits, sub_digits, mul_digits, div_digits)

    # 生成题目
    oral_gen = OralQuestionGenerator()
    vertical_gen = VerticalQuestionGenerator()
    fill_gen = FillBlankGenerator()
    list_gen = ListVerticalGenerator()

    click.echo(f"生成题目...")
    oral_questions = oral_gen.generate_batch(oral_count, digit_configs=digit_configs) if oral_count > 0 else []
    vertical_questions = vertical_gen.generate_batch(vertical_count, digit_configs=digit_configs) if vertical_count > 0 else []
    fill_questions = fill_gen.generate_batch(fill_count, digit_configs=digit_configs) if fill_count > 0 else []
    list_questions = list_gen.generate_batch(list_count, digit_configs=digit_configs) if list_count > 0 else []

    click.echo(f"生成PDF...")

    # 构建 PDF
    builder = PDFBuilder()
    builder.build(
        output_path=output_path,
        title=title,
        oral_questions=oral_questions,
        vertical_questions=vertical_questions,
        fill_questions=fill_questions,
        list_vertical_questions=list_questions,
        include_answers=include_answers
    )

    total = len(oral_questions) + len(vertical_questions) + len(fill_questions) + len(list_questions)
    click.echo(f"\n成功生成 {total} 道题目!")
    click.echo(f"文件保存到: {output_path}")


def _parse_digit_configs(difficulty, add_digits, sub_digits, mul_digits, div_digits):
    """解析位数配置"""

    # 如果指定了难度预设
    if difficulty:
        presets = {
            'easy': {
                'add': ['1x1', '2x1', '2x2'],
                'sub': ['2x1', '2x2'],
                'mul': ['1x1', '2x1'],
                'div': ['2x1']
            },
            'medium': {
                'add': ['2x2', '3x2', '3x3'],
                'sub': ['2x2', '3x2', '3x3'],
                'mul': ['2x1', '2x2', '3x1'],
                'div': ['2x1', '3x1']
            },
            'hard': {
                'add': ['3x3', '4x3', '4x4'],
                'sub': ['3x3', '4x3', '4x4'],
                'mul': ['2x2', '3x2', '4x1'],
                'div': ['3x1', '4x1', '4x2']
            }
        }
        return presets[difficulty]

    # 自定义配置
    config = {}

    if add_digits:
        config['add'] = add_digits.split(',')
    else:
        config['add'] = ['2x2', '3x2', '3x3']

    if sub_digits:
        config['sub'] = sub_digits.split(',')
    else:
        config['sub'] = ['2x2', '3x2', '3x3']

    if mul_digits:
        config['mul'] = mul_digits.split(',')
    else:
        config['mul'] = ['2x1', '2x2', '3x1']

    if div_digits:
        config['div'] = div_digits.split(',')
    else:
        config['div'] = ['2x1', '3x1']

    return config


if __name__ == '__main__':
    main()
