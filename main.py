#!/usr/bin/env python3
"""
错题卷子生成器 - CLI主程序

命令：
  scan      - 扫描图片并建立题库
  view      - 查看题库统计信息
  generate  - 生成错题练习卷PDF
  add-exam  - 添加考试记录到学生档案
  analyze   - 分析学生学习情况
  clear     - 清空题库
"""
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

from mistake_generator.config import (
    PICTURES_DIR, QUESTION_BANK_PATH, MISTAKE_PAPERS_DIR, SIMILAR_QUESTIONS_COUNT
)
from mistake_generator.image_analyzer import ImageAnalyzer
from mistake_generator.question_bank import QuestionBank
from mistake_generator.question_generator import QuestionGenerator
from mistake_generator.pdf_generator import PDFGenerator
from mistake_generator.html_generator import HTMLGenerator
from mistake_generator.student_profile import StudentProfile
from mistake_generator.learning_analyzer import LearningAnalyzer
from mistake_generator.report_generator import ReportGenerator
from knowledge_system.knowledge_base import Subject
from knowledge_system.knowledge_graph import KnowledgeGraph
from recommendation.diagnosis import DiagnosisSystem
from recommendation.daily_recommender import DailyRecommender
from recommendation.practice_generator import PracticeGenerator

console = Console()

# 初始化知识图谱（延迟加载）
_knowledge_graph = None

def get_knowledge_graph():
    global _knowledge_graph
    if _knowledge_graph is None:
        from pathlib import Path
        _knowledge_graph = KnowledgeGraph(Path("knowledge_data"))
    return _knowledge_graph


@click.group()
def cli():
    """错题卷子生成器 - 智能识别错题并生成练习卷"""
    pass


@cli.command()
@click.option('--dir', '-d', 'image_dir', type=click.Path(exists=True),
              help='图片目录路径（默认: pictures/）')
def scan(image_dir):
    """扫描图片并建立题库"""
    console.print("\n[bold cyan]开始扫描图片...[/bold cyan]\n")

    # 确定图片目录
    img_dir = Path(image_dir) if image_dir else PICTURES_DIR

    if not img_dir.exists():
        console.print(f"[red]错误：目录不存在 {img_dir}[/red]")
        return

    try:
        # 1. 分析图片
        console.print("[yellow]步骤 1/2: 分析图片识别题目...[/yellow]")
        analyzer = ImageAnalyzer()
        analysis_results = analyzer.analyze_all_images(img_dir)

        if not analysis_results:
            console.print("[red]未找到图片或分析失败[/red]")
            return

        # 2. 导入题库
        console.print("\n[yellow]步骤 2/2: 导入题库...[/yellow]")
        bank = QuestionBank(QUESTION_BANK_PATH)
        bank.import_from_analysis_results(analysis_results)

        # 显示统计信息
        console.print("\n[bold green]✓ 扫描完成！[/bold green]")
        bank.print_statistics()

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")


@cli.command()
@click.option('--type', '-t', 'question_type', help='按题型筛选')
@click.option('--mistakes-only', '-m', is_flag=True, help='仅显示错题')
def view(question_type, mistakes_only):
    """查看题库统计信息"""
    console.print("\n[bold cyan]题库信息[/bold cyan]\n")

    try:
        bank = QuestionBank(QUESTION_BANK_PATH)

        if bank.metadata['total_count'] == 0:
            console.print("[yellow]题库为空，请先运行 'scan' 命令扫描图片[/yellow]")
            return

        # 显示基本统计
        bank.print_statistics()

        # 显示详细题目列表
        if question_type or mistakes_only:
            questions = bank.get_all_questions()

            if question_type:
                questions = [q for q in questions if q.question_type == question_type]

            if mistakes_only:
                questions = [q for q in questions if q.is_mistake]

            if not questions:
                console.print(f"\n[yellow]没有找到符合条件的题目[/yellow]")
                return

            # 创建表格显示
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("题号", style="cyan")
            table.add_column("类型", style="green")
            table.add_column("内容", style="white", max_width=50)
            table.add_column("错题", justify="center")

            for q in questions[:20]:  # 最多显示20道
                content = q.question_content[:50] + "..." if len(q.question_content) > 50 else q.question_content
                is_mistake = "❌" if q.is_mistake else "✓"
                table.add_row(
                    q.question_number,
                    q.question_type,
                    content,
                    is_mistake
                )

            console.print("\n")
            console.print(table)

            if len(questions) > 20:
                console.print(f"\n[dim]... 还有 {len(questions) - 20} 道题目未显示[/dim]")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")


@cli.command()
@click.option('--output', '-o', help='输出文件名')
@click.option('--format', '-f', type=click.Choice(['html', 'pdf']), default='html',
              help='输出格式（默认: html）')
@click.option('--answers/--no-answers', default=True, help='是否包含答案页（默认: 包含）')
@click.option('--similar-count', '-n', default=SIMILAR_QUESTIONS_COUNT,
              help=f'每道错题生成的相似题数量（默认: {SIMILAR_QUESTIONS_COUNT}）')
@click.option('--type', '-t', 'question_type', help='只生成指定题型的错题')
@click.option('--limit', '-l', type=int, help='限制错题数量')
def generate(output, format, answers, similar_count, question_type, limit):
    """生成错题练习卷（HTML或PDF格式）"""
    console.print("\n[bold cyan]开始生成错题练习卷...[/bold cyan]\n")

    try:
        # 1. 加载题库
        console.print("[yellow]步骤 1/3: 加载题库...[/yellow]")
        bank = QuestionBank(QUESTION_BANK_PATH)

        if bank.metadata['total_count'] == 0:
            console.print("[red]题库为空，请先运行 'scan' 命令扫描图片[/red]")
            return

        # 获取错题
        mistakes = bank.get_mistakes()

        if not mistakes:
            console.print("[red]题库中没有错题[/red]")
            return

        # 按题型筛选
        if question_type:
            mistakes = [m for m in mistakes if m.question_type == question_type]
            if not mistakes:
                console.print(f"[red]没有找到类型为 '{question_type}' 的错题[/red]")
                return

        # 限制数量
        if limit and limit < len(mistakes):
            mistakes = mistakes[:limit]

        console.print(f"  找到 {len(mistakes)} 道错题")

        # 2. 生成相似题
        console.print(f"\n[yellow]步骤 2/3: 生成相似题（每道错题生成 {similar_count} 道）...[/yellow]")
        generator = QuestionGenerator()
        practice_set = generator.generate_practice_set(
            mistakes,
            include_original=True,
            similar_count=similar_count
        )

        # 3. 生成文档
        console.print(f"\n[yellow]步骤 3/3: 生成{format.upper()}文档...[/yellow]")

        if format == 'html':
            html_gen = HTMLGenerator(MISTAKE_PAPERS_DIR)
            file_path = html_gen.generate_mistake_paper(
                practice_set,
                output_filename=output,
                include_answers=answers
            )
        else:  # pdf
            pdf_gen = PDFGenerator(MISTAKE_PAPERS_DIR)
            file_path = pdf_gen.generate_mistake_paper(
                practice_set,
                output_filename=output,
                include_answers=answers
            )

        console.print(f"\n[bold green]✓ 错题练习卷生成成功！[/bold green]")
        console.print(f"[green]文件路径: {file_path}[/green]")

        # 统计信息
        total_questions = sum(
            1 + len(section.get("similar_questions", []))
            for sections in practice_set.values()
            for section in sections
        )
        console.print(f"[green]总题数: {total_questions}[/green]")
        console.print(f"[green]包含答案页: {'是' if answers else '否'}[/green]")
        console.print(f"[green]输出格式: {format.upper()}[/green]")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.confirmation_option(prompt='确定要清空题库吗？此操作不可恢复！')
def clear():
    """清空题库"""
    try:
        bank = QuestionBank(QUESTION_BANK_PATH)
        bank.clear()
        console.print("[green]✓ 题库已清空[/green]")
    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")


@cli.command()
@click.option('--student', '-s', required=True, help='学生姓名')
@click.option('--source', default='当前题库', help='试卷来源（如：第一单元测试）')
def add_exam(student, source):
    """将当前题库中的题目添加到学生档案"""
    console.print(f"\n[bold cyan]为学生「{student}」添加考试记录...[/bold cyan]\n")

    try:
        # 加载题库
        bank = QuestionBank(QUESTION_BANK_PATH)

        if bank.metadata['total_count'] == 0:
            console.print("[red]题库为空，请先运行 'scan' 命令扫描图片[/red]")
            return

        # 创建/加载学生档案
        profile_dir = Path("data/student_profiles")
        student_profile = StudentProfile(student, profile_dir)

        # 添加考试记录
        exam_data = {
            "source": source,
            "questions": [q.model_dump() for q in bank.get_all_questions()]
        }

        exam_record = student_profile.add_exam(exam_data)

        console.print(f"[green]✓ 考试记录已添加[/green]")
        console.print(f"[green]  试卷来源：{source}[/green]")
        console.print(f"[green]  题目数：{exam_record['total_questions']}[/green]")
        console.print(f"[green]  错题数：{exam_record['mistakes']}[/green]")
        console.print(f"[green]  正确率：{exam_record['accuracy_rate']}%[/green]")

        console.print(f"\n提示：运行 [cyan]python main.py analyze -s {student}[/cyan] 查看学习分析")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.option('--student', '-s', required=True, help='学生姓名')
@click.option('--output', '-o', help='报告输出路径')
def analyze(student, output):
    """分析学生学习情况，生成学习报告"""
    console.print(f"\n[bold cyan]分析学生「{student}」的学习情况...[/bold cyan]\n")

    try:
        # 加载学生档案
        profile_dir = Path("data/student_profiles")
        student_profile = StudentProfile(student, profile_dir)

        # 检查是否有数据
        if student_profile.data['total_questions'] == 0:
            console.print(f"[yellow]学生「{student}」还没有学习记录[/yellow]")
            console.print(f"提示：先运行 [cyan]python main.py add-exam -s {student}[/cyan] 添加考试记录")
            return

        # 分析
        analyzer = LearningAnalyzer()
        report = analyzer.analyze_student(student_profile)

        # 显示简要统计
        console.print("[bold green]✓ 分析完成！[/bold green]\n")

        console.print("[yellow]总体情况：[/yellow]")
        console.print(f"  测试次数：{report['overall_stats']['total_exams']}")
        console.print(f"  总题数：{report['overall_stats']['total_questions']}")
        console.print(f"  错题数：{report['overall_stats']['total_mistakes']}")
        console.print(f"  正确率：{report['overall_stats']['overall_accuracy']}%")

        console.print(f"\n[yellow]薄弱知识点（前3个）：[/yellow]")
        for idx, p in enumerate(report['weak_points'][:3], 1):
            console.print(f"  {idx}. {p['knowledge_point']}: {p['accuracy_rate']}% ({p['mistakes']}/{p['total']})")

        console.print(f"\n[yellow]优势知识点（前3个）：[/yellow]")
        for idx, p in enumerate(report['strong_points'][:3], 1):
            console.print(f"  {idx}. {p['knowledge_point']}: {p['accuracy_rate']}%")

        console.print(f"\n[yellow]学习趋势：[/yellow]")
        console.print(f"  {report['learning_progress'].get('message', '数据不足')}")

        # 生成HTML报告
        console.print(f"\n[yellow]正在生成HTML报告...[/yellow]")
        report_dir = Path("output/reports")
        report_gen = ReportGenerator(report_dir)

        report_path = report_gen.generate_learning_report(report, output_filename=output)

        console.print(f"\n[bold green]✓ 学习报告已生成！[/bold green]")
        console.print(f"[green]报告路径：{report_path}[/green]")
        console.print(f"\n提示：用浏览器打开报告查看详细分析和可视化图表")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.option('--student', '-s', required=True, help='学生姓名')
@click.option('--subject', type=click.Choice(['math', 'chinese', 'english']), default='math',
              help='学科（默认: math）')
@click.option('--grade', '-g', type=int, help='目标年级（默认: 学生当前年级）')
def diagnose(student, subject, grade):
    """诊断学生知识掌握情况，找出薄弱的前置知识点"""
    console.print(f"\n[bold cyan]诊断测试 - {student}[/bold cyan]\n")

    try:
        # 加载学生档案
        profile_dir = Path("data/student_profiles")
        student_profile = StudentProfile(student, profile_dir)

        if student_profile.data['total_questions'] == 0:
            console.print(f"[yellow]学生「{student}」还没有学习记录[/yellow]")
            console.print(f"提示：先运行 [cyan]python main.py add-exam -s {student}[/cyan] 添加考试记录")
            return

        # 加载知识图谱
        console.print("[yellow]加载知识图谱...[/yellow]")
        graph = get_knowledge_graph()

        # 转换学科
        subject_enum = Subject.MATH if subject == 'math' else (
            Subject.CHINESE if subject == 'chinese' else Subject.ENGLISH
        )

        # 诊断
        diagnosis_system = DiagnosisSystem(graph)
        report = diagnosis_system.diagnose_student(student_profile, subject_enum, grade or 3)

        # 显示结果
        console.print(f"\n[bold green]✓ 诊断完成！[/bold green]\n")

        console.print(f"[yellow]诊断结果：[/yellow]")
        console.print(f"  目标年级：{report['target_grade']}")
        console.print(f"  实际水平：{report['actual_grade_level']} 年级")
        console.print(f"  已掌握知识点：{report['mastered_count']} 个")
        console.print(f"  薄弱知识点：{report['weak_count']} 个")

        if report.get('root_causes'):
            console.print(f"\n[red]需要补习的前置知识点（根本原因）：[/red]")
            for idx, rc in enumerate(report['root_causes'][:5], 1):
                console.print(f"  {idx}. [{rc['grade']}年级] {rc['name']} (重要性: {rc['importance']}/5)")

        if report.get('recommendations'):
            console.print(f"\n[yellow]学习建议：[/yellow]")
            for rec in report['recommendations'][:3]:
                console.print(f"  【{rec['priority']}】{rec['title']}")
                console.print(f"      {rec['description']}")
                console.print(f"      💡 {rec['action']}")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.option('--student', '-s', required=True, help='学生姓名')
@click.option('--subject', type=click.Choice(['math', 'chinese', 'english']), default='math',
              help='学科（默认: math）')
@click.option('--grade', '-g', type=int, default=3, help='年级（默认: 3）')
def daily(student, subject, grade):
    """查看今日推荐练习方案"""
    console.print(f"\n[bold cyan]今日推荐 - {student}[/bold cyan]\n")

    try:
        # 加载学生档案
        profile_dir = Path("data/student_profiles")
        student_profile = StudentProfile(student, profile_dir)

        if student_profile.data['total_questions'] == 0:
            console.print(f"[yellow]学生「{student}」还没有学习记录[/yellow]")
            console.print(f"提示：先运行 [cyan]python main.py add-exam -s {student}[/cyan] 添加考试记录")
            return

        # 加载知识图谱
        console.print("[yellow]加载知识图谱...[/yellow]")
        graph = get_knowledge_graph()

        # 转换学科
        subject_enum = Subject.MATH if subject == 'math' else (
            Subject.CHINESE if subject == 'chinese' else Subject.ENGLISH
        )

        # 生成推荐
        recommender = DailyRecommender(graph)
        plans = recommender.recommend_daily_practice(student_profile, subject_enum, grade)

        # 显示推荐方案
        console.print(f"\n[bold green]✓ 今日推荐方案[/bold green]\n")

        for idx, plan in enumerate(plans, 1):
            priority_color = "red" if plan.get("priority") == "高" else (
                "yellow" if plan.get("priority") == "中" else "green"
            )

            console.print(f"[{priority_color}]方案 {idx}: {plan['emoji']} {plan['name']}[/{priority_color}]")
            console.print(f"  {plan['description']}")
            console.print(f"  题量：{plan['total_questions']}道 | 时间：{plan['estimated_time']}分钟 | 难度：{plan['difficulty']}")
            console.print(f"  目标：{plan['goal']}")

            if plan.get('knowledge_points'):
                console.print(f"  知识点：")
                for kp in plan['knowledge_points'][:3]:
                    console.print(f"    • {kp['name']} ({kp.get('questions_count', 5)}题)")

            console.print("")

        console.print(f"[cyan]使用方法：python main.py practice -s {student} --plan 1[/cyan]")
        console.print(f"[dim]或直接使用：python main.py practice -s {student} --auto (自动选择推荐方案)[/dim]")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
@click.option('--student', '-s', required=True, help='学生姓名')
@click.option('--plan', '-p', type=int, help='方案编号（1-4）')
@click.option('--auto', is_flag=True, help='自动选择推荐方案')
@click.option('--subject', type=click.Choice(['math', 'chinese', 'english']), default='math')
@click.option('--grade', '-g', type=int, default=3)
@click.option('--output', '-o', help='输出文件名')
def practice(student, plan, auto, subject, grade, output):
    """根据推荐方案生成练习题"""
    console.print(f"\n[bold cyan]生成练习题 - {student}[/bold cyan]\n")

    try:
        # 加载学生档案
        profile_dir = Path("data/student_profiles")
        student_profile = StudentProfile(student, profile_dir)

        # 加载知识图谱
        console.print("[yellow]加载知识图谱...[/yellow]")
        graph = get_knowledge_graph()

        subject_enum = Subject.MATH if subject == 'math' else (
            Subject.CHINESE if subject == 'chinese' else Subject.ENGLISH
        )

        # 获取推荐方案
        recommender = DailyRecommender(graph)
        plans = recommender.recommend_daily_practice(student_profile, subject_enum, grade)

        # 选择方案
        selected_plan = None

        if auto:
            # 自动选择第一个（推荐方案）
            selected_plan = plans[0] if plans else None
            console.print(f"[green]自动选择推荐方案：{selected_plan['name']}[/green]\n")
        elif plan:
            if 1 <= plan <= len(plans):
                selected_plan = plans[plan - 1]
                console.print(f"[green]选择方案{plan}：{selected_plan['name']}[/green]\n")
            else:
                console.print(f"[red]方案编号无效，请选择1-{len(plans)}[/red]")
                return
        else:
            console.print("[yellow]请指定方案编号（--plan）或使用自动模式（--auto）[/yellow]")
            console.print(f"提示：先运行 [cyan]python main.py daily -s {student}[/cyan] 查看推荐方案")
            return

        if not selected_plan:
            console.print("[red]没有可用的推荐方案[/red]")
            return

        # 生成练习题
        console.print(f"[yellow]正在生成练习题...[/yellow]")
        practice_gen = PracticeGenerator()
        questions = practice_gen.generate_practice_by_plan(selected_plan, graph)

        if not questions:
            console.print("[red]练习题生成失败[/red]")
            return

        # 生成HTML练习卷
        from mistake_generator.html_generator import HTMLGenerator

        console.print(f"\n[yellow]正在生成HTML练习卷...[/yellow]")

        # 准备练习卷数据（按知识点分组）
        practice_set = {}
        for q in questions:
            kp_name = q.get("knowledge_point", "其他")
            if kp_name not in practice_set:
                practice_set[kp_name] = []

            practice_set[kp_name].append({
                "original_question": None,
                "similar_questions": [q]
            })

        # 生成HTML
        html_gen = HTMLGenerator(MISTAKE_PAPERS_DIR)

        if not output:
            output = f"{student}_{selected_plan['name']}_{datetime.now().strftime('%Y%m%d')}.html"

        html_path = html_gen.generate_mistake_paper(
            practice_set,
            output_filename=output,
            include_answers=True
        )

        console.print(f"\n[bold green]✓ 练习卷生成成功！[/bold green]")
        console.print(f"[green]文件：{html_path}[/green]")
        console.print(f"[green]题数：{len(questions)}道[/green]")
        console.print(f"[green]方案：{selected_plan['name']}[/green]")

    except Exception as e:
        console.print(f"[red]错误: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
def info():
    """显示项目信息"""
    console.print("\n[bold cyan]智能学习系统 v2.0[/bold cyan]")
    console.print("\n核心功能：")
    console.print("  1. [green]智能识别[/green] - AI识别试卷图片中的题目和错题")
    console.print("  2. [green]题库管理[/green] - 结构化存储，知识点标注")
    console.print("  3. [green]学生分析[/green] - 追踪学习进度，识别薄弱环节")
    console.print("  4. [green]智能推荐[/green] - 每日练习自动推荐")
    console.print("  5. [green]诊断测试[/green] - 检测实际水平，回溯前置知识")
    console.print("  6. [green]练习生成[/green] - 根据推荐生成练习题")
    console.print("  7. [green]几何画图[/green] - 自动绘制几何图形")

    console.print("\n基础流程（错题卷生成）：")
    console.print("  1. [cyan]python main.py scan[/cyan] - 扫描试卷图片")
    console.print("  2. [cyan]python main.py generate[/cyan] - 生成错题练习卷")

    console.print("\n学生学习流程（智能推荐）：")
    console.print("  1. [cyan]python main.py add-exam -s 学生名[/cyan] - 添加考试记录")
    console.print("  2. [cyan]python main.py diagnose -s 学生名[/cyan] - 诊断知识掌握情况")
    console.print("  3. [cyan]python main.py daily -s 学生名[/cyan] - 查看今日推荐")
    console.print("  4. [cyan]python main.py practice -s 学生名 --auto[/cyan] - 生成练习题")
    console.print("  5. [cyan]python main.py analyze -s 学生名[/cyan] - 查看学习报告\n")

    # 检查配置
    console.print("配置检查：")
    from mistake_generator.config import ANTHROPIC_API_KEY
    if ANTHROPIC_API_KEY:
        console.print("  ✓ API密钥已配置")
    else:
        console.print("  [red]✗ 未配置API密钥，请在 .env 文件中设置 ANTHROPIC_API_KEY[/red]")

    if PICTURES_DIR.exists():
        img_count = len(list(PICTURES_DIR.glob("*.jpg"))) + len(list(PICTURES_DIR.glob("*.png")))
        console.print(f"  ✓ 图片目录存在 ({img_count} 张图片)")
    else:
        console.print(f"  [yellow]⚠ 图片目录不存在: {PICTURES_DIR}[/yellow]")

    if QUESTION_BANK_PATH.exists():
        console.print(f"  ✓ 题库文件存在")
    else:
        console.print(f"  [dim]  题库文件未创建（首次使用正常）[/dim]")


if __name__ == "__main__":
    cli()
