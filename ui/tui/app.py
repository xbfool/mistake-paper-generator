"""
TUI主应用
智能学习系统的终端界面主程序
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.binding import Binding
from textual.widgets import Header as TextualHeader, Footer as TextualFooter

from .state import AppState
from .widgets import Header, Sidebar, Footer
from .screens.dashboard import DashboardScreen
from .screens.daily import DailyScreen
from .screens.diagnose import DiagnoseScreen
from .screens.report import ReportScreen
from .screens.scan import ScanScreen


class LearningSystemApp(App):
    """智能学习系统TUI应用"""

    # CSS样式文件
    CSS_PATH = "styles.css"

    # 全局快捷键绑定
    BINDINGS = [
        Binding("q", "quit", "退出"),
        Binding("ctrl+q", "quit", "强制退出"),
        Binding("h", "help", "帮助"),
        Binding("ctrl+s", "switch_student", "切换学生"),
        Binding("ctrl+r", "refresh", "刷新"),
        Binding("1", "goto_dashboard", "主页"),
        Binding("2", "goto_daily", "推荐"),
        Binding("3", "goto_diagnose", "诊断"),
        Binding("4", "goto_report", "报告"),
        Binding("5", "goto_scan", "扫描"),
        Binding("6", "goto_students", "学生"),
        Binding("7", "goto_settings", "设置"),
    ]

    # 应用标题
    TITLE = "智能学习系统 v2.0"

    def __init__(self):
        """初始化应用"""
        super().__init__()
        self.state = AppState()
        self.current_screen_name = "dashboard"

    def compose(self) -> ComposeResult:
        """组合主界面"""
        # 顶部栏
        yield Header(classes="header")

        # 主内容区（侧边栏 + 内容）
        with Horizontal():
            # 侧边栏
            yield Sidebar(classes="sidebar")

            # 内容区（初始显示Dashboard）
            with Container(classes="content", id="main-content"):
                yield DashboardScreen()

        # 底部栏
        yield Footer(classes="footer")

    def on_mount(self) -> None:
        """应用挂载时初始化"""
        self.title = self.TITLE

        # 加载初始数据
        try:
            self.state.load_student_profile()
            self.state.load_knowledge_graph()
            self.update_footer_status(f"欢迎回来，{self.state.current_student}！")
        except Exception as e:
            self.update_footer_status(f"警告: 数据加载失败 - {e}")

    def on_sidebar_menu_selected(self, message: Sidebar.MenuSelected) -> None:
        """处理侧边栏菜单选择"""
        self.navigate_to(message.screen_name)

    def navigate_to(self, screen_name: str) -> None:
        """导航到指定屏幕"""
        self.current_screen_name = screen_name

        # 更新侧边栏高亮
        sidebar = self.query_one(Sidebar)
        sidebar.highlight_active(screen_name)

        # 切换到对应的界面
        screen_map = {
            "dashboard": DashboardScreen,
            "daily": DailyScreen,
            "diagnose": DiagnoseScreen,
            "report": ReportScreen,
            "scan": ScanScreen,
        }

        screen_class = screen_map.get(screen_name)

        if screen_class:
            try:
                self.push_screen(screen_class())
                self.update_footer_status(f"已切换到：{screen_name}")
            except Exception as e:
                self.update_footer_status(f"切换失败: {e}")
        else:
            self.update_footer_status(f"界面「{screen_name}」开发中...")

    # 快捷键动作
    def action_goto_dashboard(self) -> None:
        """跳转到主页"""
        self.navigate_to("dashboard")

    def action_goto_daily(self) -> None:
        """跳转到每日推荐"""
        self.navigate_to("daily")

    def action_goto_diagnose(self) -> None:
        """跳转到诊断测试"""
        self.navigate_to("diagnose")

    def action_goto_report(self) -> None:
        """跳转到学习报告"""
        self.navigate_to("report")

    def action_goto_scan(self) -> None:
        """跳转到扫描试卷"""
        self.navigate_to("scan")

    def action_goto_students(self) -> None:
        """跳转到学生管理"""
        self.navigate_to("students")

    def action_goto_settings(self) -> None:
        """跳转到设置"""
        self.navigate_to("settings")

    def action_switch_student(self) -> None:
        """切换学生"""
        # TODO: 弹出学生选择对话框
        self.update_footer_status("切换学生功能开发中...")

    def action_refresh(self) -> None:
        """刷新数据"""
        try:
            self.state.load_student_profile()
            self.state.load_knowledge_graph()
            self.update_footer_status("数据已刷新")
        except Exception as e:
            self.update_footer_status(f"刷新失败: {e}")

    def action_help(self) -> None:
        """显示帮助"""
        # TODO: 显示帮助对话框
        self.update_footer_status("帮助：使用数字键1-7快速导航，Q退出")

    def update_footer_status(self, message: str) -> None:
        """更新底部状态栏消息"""
        footer = self.query_one(Footer)
        footer.update_status(message)


if __name__ == "__main__":
    app = LearningSystemApp()
    app.run()
