"""
Header组件 - 顶部栏
显示应用标题、当前学生、日期时间
"""
from datetime import datetime
from textual.app import ComposeResult
from textual.widgets import Static
from textual.containers import Horizontal


class Header(Static):
    """顶部栏组件"""

    def compose(self) -> ComposeResult:
        """组合子组件"""
        with Horizontal():
            yield Static("🎓 智能学习系统 v2.0", classes="header-title")
            yield Static("", id="header-student", classes="header-student")
            yield Static("", id="header-time", classes="header-time")

    def on_mount(self) -> None:
        """挂载时初始化"""
        self.update_student()
        self.update_time()
        self.set_interval(1, self.update_time)  # 每秒更新时间

    def update_student(self) -> None:
        """更新学生信息"""
        student_widget = self.query_one("#header-student")
        student = self.app.state.current_student
        subject = self.app.state.current_subject.value
        grade = self.app.state.current_grade
        student_widget.update(f"学生: {student} | {subject} {grade}年级")

    def update_time(self) -> None:
        """更新时间显示"""
        time_widget = self.query_one("#header-time")
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_widget.update(time_str)
