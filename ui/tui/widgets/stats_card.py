"""
统计卡片组件
显示单个统计数据（如总题数、错题数等）
"""
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Vertical


class StatsCard(Static):
    """统计卡片"""

    def __init__(self, title: str, value: str, icon: str = "📊", **kwargs):
        """
        初始化统计卡片

        Args:
            title: 标题
            value: 数值
            icon: 图标
        """
        super().__init__(**kwargs)
        self.title = title
        self.value = value
        self.icon = icon

    def compose(self) -> ComposeResult:
        """组合元素"""
        yield Static(f"{self.icon}", classes="stats-icon")
        yield Static(f"{self.title}", classes="stats-label")
        yield Static(f"[bold]{self.value}[/bold]", classes="stats-value")

    def update_value(self, value: str) -> None:
        """更新数值"""
        self.value = value
        value_widget = self.query_one(".stats-value")
        value_widget.update(f"[bold]{value}[/bold]")
