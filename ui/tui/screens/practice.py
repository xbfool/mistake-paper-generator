"""
练习答题界面 - 完整集成
"""
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Input, Label, ProgressBar
from textual.containers import Container, Vertical, Horizontal
from textual.binding import Binding


class PracticeScreen(Screen):
    """练习答题界面"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "返回"),
        Binding("s", "skip_question", "跳过"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = []
        self.current_index = 0
        self.correct_count = 0
        self.wrong_count = 0
        self.start_time = None

    def compose(self) -> ComposeResult:
        """组合界面"""
        with Container():
            # 标题和进度
            yield Label("✍️ 练习中", id="title", classes="card-title")
            yield Label("", id="progress-info")
            yield ProgressBar(total=100, show_eta=False, id="progress-bar")

            # 题目显示
            with Vertical(classes="card question-container"):
                yield Label("", id="question-content")

            # 答案输入
            yield Label("你的答案：")
            yield Input(placeholder="请输入答案...", id="answer-input")

            # 反馈区域
            yield Static("", id="feedback")

            # 操作按钮
            with Horizontal():
                yield Button("提交答案", id="submit", variant="success")
                yield Button("跳过 [S]", id="skip", variant="default")
                yield Button("退出练习", id="quit-practice", variant="warning")

    def on_mount(self) -> None:
        """挂载时初始化"""
        # 获取练习题
        self.load_practice_questions()

        if self.questions:
            self.show_question(0)
        else:
            self.query_one("#question-content").update("暂无练习题")

    def load_practice_questions(self) -> None:
        """加载练习题"""
        try:
            # 从state获取选中的方案
            selected_plan = self.app.state.selected_plan

            if not selected_plan:
                # 没有选中方案，生成默认练习
                self.notify("正在生成练习题...", severity="information")

                # TODO: 调用练习生成逻辑
                # 临时：使用示例数据
                self.questions = [
                    {
                        "question_content": "7 × 8 = ?",
                        "correct_answer": "56",
                        "knowledge_point": "乘法口诀",
                        "explanation": "7 × 8 = 56"
                    },
                    {
                        "question_content": "9 × 6 = ?",
                        "correct_answer": "54",
                        "knowledge_point": "乘法口诀",
                        "explanation": "9 × 6 = 54"
                    },
                ]
            else:
                # 使用选中方案生成题目
                self.notify(f"正在生成「{selected_plan['name']}」练习题...", severity="information")

                # TODO: 根据方案生成题目
                # 临时使用示例
                count = selected_plan.get('total_questions', 10)
                self.questions = [
                    {
                        "question_content": f"示例题目 {i+1}",
                        "correct_answer": str(i+1),
                        "knowledge_point": "测试",
                        "explanation": f"答案是 {i+1}"
                    }
                    for i in range(count)
                ]

        except Exception as e:
            self.notify(f"加载练习题失败: {e}", severity="error")
            self.questions = []

    def show_question(self, index: int) -> None:
        """显示题目"""
        if index >= len(self.questions):
            # 练习结束
            self.show_summary()
            return

        self.current_index = index
        question = self.questions[index]

        # 更新进度
        progress = f"进度: {index + 1}/{len(self.questions)}"
        self.query_one("#progress-info").update(progress)

        # 更新进度条
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        progress_bar.update(total=len(self.questions), progress=index)

        # 显示题目
        q_text = f"第 {index + 1} 题\n\n{question['question_content']}\n\n知识点: {question.get('knowledge_point', '未知')}"
        self.query_one("#question-content").update(q_text)

        # 清空答案和反馈
        self.query_one("#answer-input", Input).value = ""
        self.query_one("#feedback").update("")

        # 聚焦到答案输入框
        self.query_one("#answer-input", Input).focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """按钮点击"""
        if event.button.id == "submit":
            self.check_answer()
        elif event.button.id == "skip":
            self.action_skip_question()
        elif event.button.id == "quit-practice":
            self.app.pop_screen()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """输入框回车"""
        if event.input.id == "answer-input":
            self.check_answer()

    def check_answer(self) -> None:
        """检查答案"""
        answer_input = self.query_one("#answer-input", Input)
        user_answer = answer_input.value.strip()

        if not user_answer:
            self.notify("请输入答案", severity="warning")
            return

        question = self.questions[self.current_index]
        correct_answer = str(question['correct_answer']).strip()

        feedback_widget = self.query_one("#feedback")

        if user_answer.lower() == correct_answer.lower():
            # 答对了
            self.correct_count += 1
            feedback_widget.update(
                f"[green]✅ 回答正确！[/green]\n\n"
                f"你的答案: {user_answer}\n"
                f"解析: {question.get('explanation', '暂无解析')}"
            )
            self.notify("✅ 正确！", severity="information")
        else:
            # 答错了
            self.wrong_count += 1
            feedback_widget.update(
                f"[red]❌ 回答错误[/red]\n\n"
                f"你的答案: {user_answer}\n"
                f"正确答案: {correct_answer}\n"
                f"解析: {question.get('explanation', '暂无解析')}"
            )
            self.notify("❌ 错误", severity="warning")

        # 2秒后自动下一题
        self.set_timer(2, self.next_question)

    def next_question(self) -> None:
        """下一题"""
        self.show_question(self.current_index + 1)

    def action_skip_question(self) -> None:
        """跳过当前题"""
        self.show_question(self.current_index + 1)

    def show_summary(self) -> None:
        """显示练习总结"""
        total = len(self.questions)
        accuracy = (self.correct_count / total * 100) if total > 0 else 0

        summary = f"""
🎉 练习完成！

📊 本次练习统计
━━━━━━━━━━━━━━━━━━
总题数: {total} 道
正确:  {self.correct_count} 道
错误:  {self.wrong_count} 道
正确率: {accuracy:.1f}%

[按 Escape 或 Q 返回主页]
"""

        self.query_one("#question-content").update(summary)
        self.query_one("#progress-info").update("练习完成")
        self.query_one("#answer-input", Input).disabled = True
        self.query_one("#submit", Button).disabled = True
        self.query_one("#skip", Button).disabled = True

        # 更新进度条为100%
        progress_bar = self.query_one("#progress-bar", ProgressBar)
        progress_bar.update(progress=total)

        # TODO: 保存练习记录到学生档案

        self.notify(f"练习完成！正确率: {accuracy:.1f}%", severity="information")
