"""
Sidebar组件 - 侧边导航栏
"""
from textual.app import ComposeResult
from textual.widgets import Button
from textual.containers import VerticalScroll, Vertical
from textual.message import Message


class Sidebar(VerticalScroll):
    """侧边导航栏"""

    # 菜单项配置
    MENU_ITEMS = [
        ("dashboard", "🏠 主页", "1"),
        ("daily", "📅 今日推荐", "2"),
        ("diagnose", "🔍 诊断测试", "3"),
        ("report", "📊 学习报告", "4"),
        ("scan", "📷 扫描试卷", "5"),
        ("students", "👥 学生管理", "6"),
        ("settings", "⚙️ 设置", "7"),
    ]

    class MenuSelected(Message):
        """菜单选中消息"""

        def __init__(self, screen_name: str) -> None:
            self.screen_name = screen_name
            super().__init__()

    def compose(self) -> ComposeResult:
        """组合菜单项"""
        with Vertical():
            yield Button("", id="menu-spacer", disabled=True, variant="primary")

            for screen_name, label, key in self.MENU_ITEMS:
                button = Button(
                    f"{label}  [{key}]",
                    id=f"menu-{screen_name}",
                    classes="menu-item"
                )
                button.screen_name = screen_name  # 自定义属性
                yield button

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        if hasattr(event.button, 'screen_name'):
            # 发送菜单选中消息
            self.post_message(self.MenuSelected(event.button.screen_name))

    def highlight_active(self, screen_name: str) -> None:
        """高亮当前激活的菜单项"""
        # 移除所有active类
        for button in self.query(Button):
            button.remove_class("menu-item-active")

        # 添加active类到当前项
        active_button = self.query_one(f"#menu-{screen_name}", Button)
        if active_button:
            active_button.add_class("menu-item-active")
