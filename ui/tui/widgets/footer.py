"""
Footer组件 - 底部状态栏
显示快捷键提示和状态信息
"""
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal


class Footer(Static):
    """底部状态栏"""

    def compose(self) -> ComposeResult:
        """组合子组件"""
        with Horizontal():
            yield Static("", id="footer-status", classes="footer-status")
            yield Static("", id="footer-keybindings", classes="footer-keybindings")

    def on_mount(self) -> None:
        """挂载时初始化"""
        self.update_keybindings()

    def update_keybindings(self, custom_keys: str = None) -> None:
        """更新快捷键提示"""
        keybindings_widget = self.query_one("#footer-keybindings")

        if custom_keys:
            keybindings_widget.update(custom_keys)
        else:
            # 默认快捷键
            default_keys = "[Q]退出 [H]帮助 [Ctrl+S]切换学生 [Ctrl+R]刷新"
            keybindings_widget.update(default_keys)

    def update_status(self, message: str) -> None:
        """更新状态信息"""
        status_widget = self.query_one("#footer-status")
        status_widget.update(f"📌 {message}")
