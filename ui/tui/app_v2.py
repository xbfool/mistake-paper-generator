"""
TUI主应用 v2 - 修复版
完整集成所有功能，优化导航体验
"""
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import Screen

from .state import AppState
from .screens.dashboard import DashboardScreen
from .screens.daily import DailyScreen
from .screens.diagnose import DiagnoseScreen
from .screens.report import ReportScreen
from .screens.scan import ScanScreen


class LearningSystemApp(App):
    """智能学习系统TUI应用"""

    CSS_PATH = "styles.css"
    TITLE = "智能学习系统 v2.0"

    # 注册所有屏幕
    SCREENS = {
        "dashboard": DashboardScreen,
        "daily": DailyScreen,
        "diagnose": DiagnoseScreen,
        "report": ReportScreen,
        "scan": ScanScreen,
    }

    # 全局快捷键
    BINDINGS = [
        Binding("q", "quit", "退出", priority=True),
        Binding("1", "switch_screen('dashboard')", "主页"),
        Binding("2", "switch_screen('daily')", "推荐"),
        Binding("3", "switch_screen('diagnose')", "诊断"),
        Binding("4", "switch_screen('report')", "报告"),
        Binding("5", "switch_screen('scan')", "扫描"),
        Binding("r", "refresh", "刷新"),
    ]

    def __init__(self):
        super().__init__()
        self.state = AppState()

    def on_mount(self) -> None:
        """应用挂载"""
        # 加载初始数据
        try:
            self.state.load_student_profile()
            self.state.load_knowledge_graph()
        except Exception as e:
            self.notify(f"数据加载失败: {e}", severity="warning")

        # 显示Dashboard
        self.push_screen("dashboard")

    def action_refresh(self) -> None:
        """刷新数据"""
        try:
            self.state.load_student_profile()
            self.state.load_knowledge_graph()
            self.notify("数据已刷新", severity="information")

            # 刷新当前屏幕
            if self.screen:
                if hasattr(self.screen, 'on_refresh'):
                    self.screen.on_refresh()
        except Exception as e:
            self.notify(f"刷新失败: {e}", severity="error")


if __name__ == "__main__":
    app = LearningSystemApp()
    app.run()
