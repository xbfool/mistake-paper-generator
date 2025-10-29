"""
Dashboard主面板
显示学生学习概况和快捷操作
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label
from textual.containers import Container, Vertical, Horizontal, Grid
from textual.reactive import reactive


class DashboardScreen(Screen):
    """Dashboard主面板"""

    # 响应式属性
    total_questions = reactive(0)
    total_mistakes = reactive(0)
    accuracy_rate = reactive(0.0)
    grade_level = reactive("0.0")

    def compose(self) -> ComposeResult:
        """组合界面元素"""
        with Container():
            yield Label("📊 今日概况", classes="card-title")

            # 统计卡片（使用ID以便后续更新）
            with Grid(id="stats-grid"):
                yield Static("[bold]总题数[/bold]\n0", id="stat-total", classes="stats-card")
                yield Static("[bold]错题数[/bold]\n0", id="stat-mistakes", classes="stats-card")
                yield Static("[bold]正确率[/bold]\n0%", id="stat-accuracy", classes="stats-card")
                yield Static("[bold]实际水平[/bold]\n-年级", id="stat-level", classes="stats-card")

            yield Label("🎯 今日推荐", classes="card-title")

            # 推荐方案卡片
            with Vertical(classes="card plan-recommended", id="recommended-plan"):
                yield Label("加载中...", id="plan-content")
                with Horizontal():
                    yield Button("立即开始", id="start-practice", variant="success")

            yield Label("🔴 薄弱知识点 Top 3", classes="card-title")

            # 薄弱知识点列表
            with Vertical(classes="card", id="weak-points-container"):
                yield Label("加载中...", id="weak-points-list")

            yield Label("⚡ 快捷操作", classes="card-title")

            # 快捷操作按钮
            with Horizontal():
                yield Button("[D]诊断", id="quick-diagnose", variant="primary")
                yield Button("[R]推荐", id="quick-daily", variant="default")
                yield Button("[P]练习", id="quick-practice", variant="success")
                yield Button("[A]分析", id="quick-analyze", variant="default")

    def on_mount(self) -> None:
        """挂载时加载数据"""
        self.load_data()

    def load_data(self) -> None:
        """加载学生数据"""
        try:
            # 加载学生档案
            self.app.state.load_student_profile()
            profile = self.app.state.student_profile

            if profile and profile.data.get('total_questions', 0) > 0:
                # 更新统计数据
                self.total_questions = profile.data['total_questions']
                self.total_mistakes = profile.data['total_mistakes']
                overall_stats = profile.get_overall_stats()
                self.accuracy_rate = overall_stats['overall_accuracy']

                # 更新界面
                self.query_one("#stat-total").update(f"[bold]总题数[/bold]\n{self.total_questions}")
                self.query_one("#stat-mistakes").update(f"[bold]错题数[/bold]\n{self.total_mistakes}")
                self.query_one("#stat-accuracy").update(f"[bold]正确率[/bold]\n{self.accuracy_rate:.1f}%")

                # TODO: 从诊断结果获取实际水平
                self.query_one("#stat-level").update(f"[bold]实际水平[/bold]\n需诊断")

                # 加载薄弱知识点
                weak_points = profile.get_weak_knowledge_points(threshold=70.0, min_count=2)
                self.update_weak_points(weak_points[:3])

                # 显示推荐
                self.query_one("#plan-content").update("⭐ 查看「每日推荐」获取个性化练习方案")
            else:
                # 没有学习数据
                self.query_one("#plan-content").update("📝 还没有学习记录，请先扫描试卷")
                self.query_one("#weak-points-list").update("暂无数据")

        except Exception as e:
            self.query_one("#plan-content").update(f"加载失败: {e}")

    def update_weak_points(self, weak_points: list) -> None:
        """更新薄弱知识点显示"""
        weak_list = self.query_one("#weak-points-list")

        if not weak_points:
            weak_list.update("✅ 暂无薄弱知识点，继续保持！")
            return

        lines = []
        for idx, point in enumerate(weak_points, 1):
            accuracy = point['accuracy_rate']
            name = point['knowledge_point']
            mistakes = point['mistakes']
            total = point['total']

            # 生成进度条
            progress_blocks = int(accuracy / 10)
            progress_bar = "█" * progress_blocks + "░" * (10 - progress_blocks)

            # 颜色
            if accuracy < 40:
                color = "red"
            elif accuracy < 70:
                color = "yellow"
            else:
                color = "cyan"

            lines.append(f"{idx}. {name:12s} {accuracy:5.1f}%  [{color}]{progress_bar}[/{color}]  ({mistakes}/{total})")

        weak_list.update("\n".join(lines))

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击事件"""
        button_id = event.button.id

        if button_id == "start-practice":
            # 跳转到每日推荐
            self.app.action_goto_daily()
        elif button_id == "quick-diagnose":
            self.app.action_goto_diagnose()
        elif button_id == "quick-daily":
            self.app.action_goto_daily()
        elif button_id == "quick-practice":
            self.app.action_goto_daily()
        elif button_id == "quick-analyze":
            self.app.action_goto_report()

