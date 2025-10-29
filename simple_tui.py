#!/usr/bin/env python3
"""
智能学习系统 - 简化TUI版本
修复所有导航问题，清晰简洁
"""
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.widgets import Header, Footer, Button, Static, Label
from textual.binding import Binding
from textual.screen import Screen

# 导入核心功能
from mistake_generator.student_profile import StudentProfile
from knowledge_system.knowledge_base import Subject
from knowledge_system.knowledge_graph import KnowledgeGraph


class MainScreen(Screen):
    """主屏幕 - 所有功能都在这里"""

    BINDINGS = [
        ("q", "quit", "退出"),
        ("d", "show_diagnose", "诊断"),
        ("r", "show_daily", "推荐"),
        ("a", "show_report", "报告"),
    ]

    def __init__(self, student_name="琪琪"):
        super().__init__()
        self.student_name = student_name
        self.profile = None
        self.graph = None

    def compose(self) -> ComposeResult:
        """组合界面"""
        yield Header(show_clock=True)

        with Container():
            # 学生信息
            yield Label(f"🎓 学生: {self.student_name} | 数学 3年级", id="student-info")
            yield Label("")

            # 统计卡片
            yield Label("📊 学习概况")
            with Grid(id="stats-grid", classes="stats-container"):
                yield Static("[bold]总题数[/bold]\n-", id="stat-total")
                yield Static("[bold]错题数[/bold]\n-", id="stat-mistakes")
                yield Static("[bold]正确率[/bold]\n-%", id="stat-accuracy")
                yield Static("[bold]实际水平[/bold]\n-年级", id="stat-level")

            yield Label("")

            # 薄弱知识点
            yield Label("🔴 薄弱知识点")
            yield Static("加载中...", id="weak-points")

            yield Label("")

            # 操作按钮
            yield Label("⚡ 快捷操作")
            with Horizontal():
                yield Button("[D] 诊断测试", id="btn-diagnose", variant="primary")
                yield Button("[R] 今日推荐", id="btn-daily", variant="success")
                yield Button("[A] 学习报告", id="btn-report", variant="default")

            yield Label("")
            yield Label("💡 提示: 使用字母快捷键快速操作", id="tip")

        yield Footer()

    def on_mount(self) -> None:
        """挂载时加载数据"""
        self.load_data()

    def load_data(self) -> None:
        """加载学生数据"""
        try:
            # 加载学生档案
            profile_dir = Path("data/student_profiles")
            self.profile = StudentProfile(self.student_name, profile_dir)

            # 加载知识图谱
            self.graph = KnowledgeGraph(Path("knowledge_data"))

            # 更新统计
            if self.profile.data.get('total_questions', 0) > 0:
                stats = self.profile.get_overall_stats()

                self.query_one("#stat-total").update(
                    f"[bold]总题数[/bold]\n{stats['total_questions']}"
                )
                self.query_one("#stat-mistakes").update(
                    f"[bold]错题数[/bold]\n{stats['total_mistakes']}"
                )
                self.query_one("#stat-accuracy").update(
                    f"[bold]正确率[/bold]\n{stats['overall_accuracy']:.1f}%"
                )

                # 薄弱知识点
                weak_points = self.profile.get_weak_knowledge_points(threshold=70.0, min_count=2)
                if weak_points:
                    lines = []
                    for idx, point in enumerate(weak_points[:5], 1):
                        accuracy = point['accuracy_rate']
                        name = point['knowledge_point']
                        progress = "█" * int(accuracy/10) + "░" * (10 - int(accuracy/10))
                        color = "red" if accuracy < 40 else ("yellow" if accuracy < 70 else "green")
                        lines.append(f"{idx}. {name:15s} {accuracy:5.1f}% [{color}]{progress}[/{color}]")

                    self.query_one("#weak-points").update("\n".join(lines))
                else:
                    self.query_one("#weak-points").update("✅ 暂无薄弱知识点")
            else:
                self.query_one("#weak-points").update("还没有学习记录")

        except Exception as e:
            self.query_one("#weak-points").update(f"加载失败: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击"""
        if event.button.id == "btn-diagnose":
            self.action_show_diagnose()
        elif event.button.id == "btn-daily":
            self.action_show_daily()
        elif event.button.id == "btn-report":
            self.action_show_report()

    def action_show_diagnose(self) -> None:
        """显示诊断"""
        self.app.push_screen(DiagnoseDetailScreen(self.profile, self.graph))

    def action_show_daily(self) -> None:
        """显示推荐"""
        self.app.push_screen(DailyRecommendScreen(self.profile, self.graph))

    def action_show_report(self) -> None:
        """显示报告"""
        self.app.push_screen(ReportDetailScreen(self.profile))


class DiagnoseDetailScreen(Screen):
    """诊断详情屏幕"""

    BINDINGS = [("escape", "app.pop_screen", "返回")]

    def __init__(self, profile, graph):
        super().__init__()
        self.profile = profile
        self.graph = graph

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("🔍 诊断测试结果", id="title")
            yield Static("正在诊断...", id="diagnose-result")
            yield Button("返回 [ESC]", id="back", variant="default")
        yield Footer()

    def on_mount(self) -> None:
        """运行诊断"""
        try:
            from recommendation.diagnosis import DiagnosisSystem

            diagnosis = DiagnosisSystem(self.graph)
            report = diagnosis.diagnose_student(self.profile, Subject.MATH, 3)

            lines = []
            lines.append(f"目标年级: {report['target_grade']} | 实际水平: {report['actual_grade_level']}年级")
            lines.append(f"已掌握: {report['mastered_count']}个 | 薄弱: {report['weak_count']}个")
            lines.append("")
            lines.append("需要补习的前置知识点：")

            for idx, rc in enumerate(report.get('root_causes', [])[:5], 1):
                lines.append(f"  {idx}. [{rc['grade']}年级] {rc['name']}")

            self.query_one("#diagnose-result").update("\n".join(lines))
        except Exception as e:
            self.query_one("#diagnose-result").update(f"诊断失败: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class DailyRecommendScreen(Screen):
    """每日推荐屏幕"""

    BINDINGS = [("escape", "app.pop_screen", "返回")]

    def __init__(self, profile, graph):
        super().__init__()
        self.profile = profile
        self.graph = graph

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("📅 今日推荐", id="title")
            yield Static("正在加载推荐...", id="daily-content")
            yield Button("返回 [ESC]", id="back", variant="default")
        yield Footer()

    def on_mount(self) -> None:
        """加载推荐"""
        try:
            from recommendation.daily_recommender import DailyRecommender

            recommender = DailyRecommender(self.graph)
            plans = recommender.recommend_daily_practice(self.profile, Subject.MATH, 3)

            lines = []
            for idx, plan in enumerate(plans, 1):
                lines.append(f"{plan['emoji']} 方案{idx}: {plan['name']}")
                lines.append(f"  {plan['description']}")
                lines.append(f"  题量: {plan['total_questions']}道 | 时间: {plan['estimated_time']}分钟")
                lines.append("")

            lines.append("💡 使用CLI生成练习：python main.py practice -s 琪琪 --auto")

            self.query_one("#daily-content").update("\n".join(lines))
        except Exception as e:
            self.query_one("#daily-content").update(f"加载失败: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class ReportDetailScreen(Screen):
    """学习报告屏幕"""

    BINDINGS = [("escape", "app.pop_screen", "返回")]

    def __init__(self, profile):
        super().__init__()
        self.profile = profile

    def compose(self) -> ComposeResult:
        yield Header()
        with Container():
            yield Label("📊 学习报告", id="title")
            yield Static("加载中...", id="report-content")
            yield Button("返回 [ESC]", id="back", variant="default")
        yield Footer()

    def on_mount(self) -> None:
        """加载报告"""
        try:
            stats = self.profile.get_overall_stats()
            weak = self.profile.get_weak_knowledge_points()
            strong = self.profile.get_strong_knowledge_points()

            lines = []
            lines.append(f"测试次数: {stats['total_exams']}")
            lines.append(f"总题数: {stats['total_questions']}")
            lines.append(f"正确率: {stats['overall_accuracy']}%")
            lines.append("")

            lines.append("🔴 薄弱知识点:")
            for idx, p in enumerate(weak[:5], 1):
                lines.append(f"  {idx}. {p['knowledge_point']:15s} {p['accuracy_rate']:.1f}%")

            self.query_one("#report-content").update("\n".join(lines))
        except Exception as e:
            self.query_one("#report-content").update(f"加载失败: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()


class SimpleTUIApp(App):
    """简化版TUI应用"""

    BINDINGS = [
        ("q", "quit", "退出"),
        ("d", "diagnose", "诊断"),
        ("r", "daily", "推荐"),
        ("a", "report", "报告"),
    ]

    def __init__(self, student_name="琪琪"):
        super().__init__()
        self.student_name = student_name

    def on_mount(self) -> None:
        """启动"""
        self.push_screen(MainScreen(self.student_name))

    def action_diagnose(self) -> None:
        """诊断"""
        screen = self.screen
        if isinstance(screen, MainScreen):
            screen.action_show_diagnose()

    def action_daily(self) -> None:
        """推荐"""
        screen = self.screen
        if isinstance(screen, MainScreen):
            screen.action_show_daily()

    def action_report(self) -> None:
        """报告"""
        screen = self.screen
        if isinstance(screen, MainScreen):
            screen.action_show_report()


if __name__ == "__main__":
    app = SimpleTUIApp(student_name="琪琪")
    app.run()
