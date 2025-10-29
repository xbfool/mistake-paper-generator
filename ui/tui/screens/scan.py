"""
扫描试卷界面（简化版）
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.containers import Container, Vertical, Horizontal


class ScanScreen(Screen):
    """扫描试卷界面"""

    BINDINGS = [("b", "pop_screen", "返回")]

    def compose(self) -> ComposeResult:
        with Container():
            yield Label("📷 扫描试卷", classes="card-title")

            with Vertical(classes="card"):
                yield Label("扫描试卷功能")
                yield Label("")
                yield Label("使用CLI命令扫描：")
                yield Label("  python3 main.py scan")
                yield Label("")
                yield Label("扫描后使用以下命令添加到学生档案：")
                yield Label(f"  python3 main.py add-exam -s {self.app.state.current_student}")

            with Horizontal():
                yield Button("返回", id="back", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
