"""
学习报告界面
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.containers import Container, ScrollableContainer, Horizontal


class ReportScreen(Screen):
    """学习报告界面"""

    BINDINGS = [("b", "pop_screen", "返回")]

    def compose(self) -> ComposeResult:
        """组合界面"""
        with Container():
            yield Label(f"📊 学习报告 - {self.app.state.current_student}", classes="card-title")

            with ScrollableContainer(id="report-container"):
                yield Static("加载中...", id="report-content")

            with Horizontal():
                yield Button("生成HTML报告", id="export-html", variant="primary")
                yield Button("返回", id="back", variant="default")

    def on_mount(self) -> None:
        """挂载时加载报告"""
        self.load_report()

    def load_report(self) -> None:
        """加载学习报告"""
        try:
            self.app.state.load_student_profile()
            profile = self.app.state.student_profile

            if not profile or profile.data.get('total_questions', 0) == 0:
                self.query_one("#report-content").update("还没有学习记录")
                return

            # 获取统计数据
            overall_stats = profile.get_overall_stats()
            weak_points = profile.get_weak_knowledge_points(threshold=70.0)
            strong_points = profile.get_strong_knowledge_points(threshold=85.0)
            progress = profile.get_learning_progress()

            # 格式化显示
            lines = []
            lines.append("📈 总体统计")
            lines.append("━" * 40)
            lines.append(f"测试次数: {overall_stats['total_exams']}")
            lines.append(f"累计题数: {overall_stats['total_questions']}")
            lines.append(f"错题数量: {overall_stats['total_mistakes']}")
            lines.append(f"总体正确率: {overall_stats['overall_accuracy']}%")
            lines.append(f"学习趋势: {progress.get('message', '数据不足')}")
            lines.append("")

            lines.append("🔴 薄弱知识点")
            lines.append("━" * 40)
            if weak_points:
                for idx, point in enumerate(weak_points[:10], 1):
                    lines.append(
                        f"{idx}. {point['knowledge_point']:15s} {point['accuracy_rate']:5.1f}% "
                        f"({point['mistakes']}/{point['total']})"
                    )
            else:
                lines.append("✅ 暂无薄弱知识点")
            lines.append("")

            lines.append("🟢 掌握良好的知识点")
            lines.append("━" * 40)
            if strong_points:
                for idx, point in enumerate(strong_points[:10], 1):
                    lines.append(f"{idx}. {point['knowledge_point']:15s} {point['accuracy_rate']:5.1f}%")
            else:
                lines.append("暂无数据")

            self.query_one("#report-content").update("\n".join(lines))

        except Exception as e:
            self.query_one("#report-content").update(f"加载失败: {e}")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击"""
        if event.button.id == "export-html":
            # TODO: 生成HTML报告
            footer = self.app.query_one("Footer")
            footer.update_status("使用CLI命令生成HTML报告：python main.py analyze -s 琪琪")
        elif event.button.id == "back":
            self.app.pop_screen()
