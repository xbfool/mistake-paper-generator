"""
诊断测试界面
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.containers import Container, Vertical, Horizontal


class DiagnoseScreen(Screen):
    """诊断测试界面"""

    BINDINGS = [("b", "pop_screen", "返回")]

    def compose(self) -> ComposeResult:
        """组合界面"""
        with Container():
            yield Label(f"🔍 诊断测试 - {self.app.state.current_student}", classes="card-title")

            with Vertical(classes="card"):
                yield Label("正在分析...", id="diagnose-status")
                yield Static("", id="diagnose-result")

            with Horizontal():
                yield Button("开始补习", id="start-remedial", variant="success")
                yield Button("返回", id="back", variant="default")

    def on_mount(self) -> None:
        """挂载时运行诊断"""
        self.run_diagnosis()

    def run_diagnosis(self) -> None:
        """运行诊断"""
        try:
            from recommendation.diagnosis import DiagnosisSystem

            self.app.state.load_student_profile()
            self.app.state.load_knowledge_graph()

            profile = self.app.state.student_profile
            graph = self.app.state.knowledge_graph

            if not profile or profile.data.get('total_questions', 0) == 0:
                self.query_one("#diagnose-result").update("还没有学习记录")
                return

            # 诊断
            diagnosis = DiagnosisSystem(graph)
            report = diagnosis.diagnose_student(
                profile,
                self.app.state.current_subject,
                self.app.state.current_grade
            )

            # 显示结果
            self.display_result(report)

        except Exception as e:
            self.query_one("#diagnose-result").update(f"诊断失败: {e}")

    def display_result(self, report: dict) -> None:
        """显示诊断结果"""
        result_widget = self.query_one("#diagnose-result")

        lines = []
        lines.append(f"目标年级: {report['target_grade']} | 实际水平: {report['actual_grade_level']}年级")
        lines.append(f"已掌握: {report['mastered_count']}个 | 薄弱: {report['weak_count']}个")
        lines.append("")

        if report.get('root_causes'):
            lines.append("需要补习的前置知识点：")
            for idx, rc in enumerate(report['root_causes'][:5], 1):
                stars = "★" * rc['importance']
                lines.append(f"  {idx}. [{rc['grade']}年级] {rc['name']} ({stars})")

        result_widget.update("\n".join(lines))
        self.query_one("#diagnose-status").update("✓ 诊断完成")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击"""
        if event.button.id == "start-remedial":
            self.app.action_goto_daily()
        elif event.button.id == "back":
            self.app.pop_screen()
