"""
薄弱知识点列表组件
"""
from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import Vertical


class WeakPointsList(Vertical):
    """薄弱知识点列表"""

    def __init__(self, weak_points: list, **kwargs):
        """
        初始化薄弱知识点列表

        Args:
            weak_points: 薄弱知识点列表，格式：
                [{"name": "乘法应用", "accuracy_rate": 0.0, "total": 4, "mistakes": 4}, ...]
        """
        super().__init__(**kwargs)
        self.weak_points = weak_points

    def compose(self) -> ComposeResult:
        """组合元素"""
        if not self.weak_points:
            yield Label("✅ 暂无薄弱知识点，继续保持！", classes="success-message")
            return

        for idx, point in enumerate(self.weak_points[:5], 1):  # 最多显示5个
            accuracy = point.get("accuracy_rate", 0)
            name = point.get("name", "未知")
            mistakes = point.get("mistakes", 0)
            total = point.get("total", 0)

            # 生成进度条
            progress_blocks = int(accuracy / 10)
            progress_bar = "█" * progress_blocks + "░" * (10 - progress_blocks)

            # 颜色编码
            if accuracy < 40:
                color = "red"
            elif accuracy < 70:
                color = "yellow"
            else:
                color = "cyan"

            # 格式化显示
            text = f"{idx}. {name:12s} {accuracy:5.1f}%  [{color}]{progress_bar}[/{color}]  ({mistakes}/{total})"

            yield Label(text, classes="knowledge-point-item")
