"""
每日推荐界面
显示推荐的练习方案供用户选择
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label, RadioButton, RadioSet
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer


class DailyScreen(Screen):
    """每日推荐界面"""

    BINDINGS = [
        ("b", "pop_screen", "返回"),
        ("enter", "start_practice", "开始练习"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plans = []
        self.selected_plan_index = 0

    def compose(self) -> ComposeResult:
        """组合界面"""
        with Container():
            yield Label(f"📅 今日推荐 - {self.app.state.current_student}", classes="card-title")

            yield Label("请选择练习方案：")

            # 推荐方案列表
            with ScrollableContainer(id="plans-container"):
                yield Label("加载中...", id="plans-list")

            # 操作按钮
            with Horizontal():
                yield Button("开始练习", id="start-practice", variant="success")
                yield Button("返回", id="back", variant="default")

    def on_mount(self) -> None:
        """挂载时加载推荐"""
        self.load_recommendations()

    def load_recommendations(self) -> None:
        """加载推荐方案"""
        try:
            from recommendation.daily_recommender import DailyRecommender

            # 加载数据
            self.app.state.load_student_profile()
            self.app.state.load_knowledge_graph()

            profile = self.app.state.student_profile
            graph = self.app.state.knowledge_graph

            if not profile or profile.data.get('total_questions', 0) == 0:
                self.query_one("#plans-list").update(
                    "还没有学习记录，请先扫描试卷并添加考试记录"
                )
                return

            # 生成推荐
            recommender = DailyRecommender(graph)
            self.plans = recommender.recommend_daily_practice(
                profile,
                self.app.state.current_subject,
                self.app.state.current_grade
            )

            # 显示推荐方案
            self.display_plans()

        except Exception as e:
            self.query_one("#plans-list").update(f"加载失败: {e}")

    def display_plans(self) -> None:
        """显示推荐方案"""
        plans_widget = self.query_one("#plans-list")

        if not self.plans:
            plans_widget.update("暂无推荐方案")
            return

        lines = []

        for idx, plan in enumerate(self.plans, 1):
            # 判断是否为推荐方案
            is_recommended = plan.get('priority') == '高' or idx == 1

            # 格式化方案信息
            header = f"{'⭐' if is_recommended else '  '} 方案{idx}: {plan['emoji']} {plan['name']}"
            desc = f"     {plan['description']}"
            stats = f"     📊 {plan['total_questions']}道题 | ⏱️ {plan['estimated_time']}分钟 | 难度: {plan['difficulty']}"
            goal = f"     🎯 {plan['goal']}"

            lines.append(header)
            lines.append(desc)
            lines.append(stats)
            lines.append(goal)

            # 显示知识点（如果有）
            if plan.get('knowledge_points'):
                lines.append("     知识点：")
                for kp in plan['knowledge_points'][:3]:
                    lines.append(f"       • {kp['name']} ({kp.get('questions_count', 5)}题)")

            lines.append("")  # 空行分隔

        plans_widget.update("\n".join(lines))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击"""
        if event.button.id == "start-practice":
            self.action_start_practice()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_start_practice(self) -> None:
        """开始练习"""
        if self.plans:
            # 默认选择第一个方案
            self.app.state.selected_plan = self.plans[0]
            self.app.state.selected_plan_index = 0

            # TODO: 跳转到练习界面
            # self.app.push_screen("practice")

            # 临时：显示消息
            footer = self.app.query_one("Footer")
            footer.update_status("练习界面开发中，请使用CLI命令：python main.py practice -s 琪琪 --auto")
