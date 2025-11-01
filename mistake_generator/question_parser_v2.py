"""
双状态题目解析模块
解析首次答题和订正两种状态
"""
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field, asdict
from datetime import datetime
from .ai_provider import get_ai_provider


@dataclass
class FirstAttempt:
    """首次答题状态"""
    student_answer: Optional[str] = None
    is_correct: bool = False
    teacher_mark: Optional[str] = None  # "✓", "×", "?", 等
    deducted_points: Optional[float] = None


@dataclass
class Correction:
    """订正状态"""
    student_answer: Optional[str] = None
    is_correct: bool = False
    corrected_at: Optional[str] = None
    has_corrected: bool = False


@dataclass
class ErrorAnalysis:
    """错误分析"""
    first_attempt_reason: Optional[str] = None
    correction_quality: Optional[str] = None
    suggest_practice: bool = False


@dataclass
class QuestionV2:
    """题目数据（双状态）"""
    question_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    exam_id: Optional[str] = None
    subject: Optional[str] = None
    content: Optional[str] = None
    standard_answer: Optional[str] = None

    # 双状态
    first_attempt: FirstAttempt = field(default_factory=FirstAttempt)
    correction: Correction = field(default_factory=Correction)

    # 知识点分析
    knowledge_points: List[str] = field(default_factory=list)
    difficulty: int = 3  # 1-5
    question_type: Optional[str] = None

    # 位置信息
    page_number: Optional[int] = None
    position: Optional[str] = None

    # AI 分析
    error_analysis: ErrorAnalysis = field(default_factory=ErrorAnalysis)


class QuestionParserV2:
    """双状态题目解析器"""

    def __init__(self, ai_provider_name: Optional[str] = None):
        """
        初始化题目解析器

        Args:
            ai_provider_name: AI 提供者名称
        """
        self.ai_provider = get_ai_provider(ai_provider_name)

    def parse_graded_paper(
        self,
        image_path: Path,
        subject: str,
        exam_id: str
    ) -> List[QuestionV2]:
        """
        解析批阅后的试卷，提取题目和首次答题状态

        Args:
            image_path: 批阅卷图片路径
            subject: 科目
            exam_id: 考试ID

        Returns:
            题目列表
        """
        prompt = f"""请分析这张已批阅的{subject}试卷，提取所有题目信息。

对每道题目，请识别：
1. **题目内容**：完整的题目文字
2. **标准答案**：正确答案（如果试卷上有）
3. **学生答案**：学生的答题内容
4. **批改标记**：老师的红笔标记（✓、×、?、半对等）
5. **是否正确**：根据批改标记判断
6. **扣分**：如果有扣分标注
7. **题型**：选择题、填空题、计算题、应用题等
8. **题号**：第几题

请以 JSON 数组格式返回，每道题一个对象：
[
  {{
    "content": "计算：25 × 4 = ?",
    "standard_answer": "100",
    "student_answer": "90",
    "teacher_mark": "×",
    "is_correct": false,
    "deducted_points": 5,
    "question_type": "计算题",
    "position": "第5题"
  }},
  ...
]

只返回 JSON 数组，不要包含其他文本。"""

        try:
            # 使用 AI 分析图像
            response_text = self.ai_provider.analyze_image(
                image_path=image_path,
                prompt=prompt
            )

            # 解析 JSON
            response_text = self._clean_json_response(response_text)
            questions_data = json.loads(response_text)

            # 转换为 QuestionV2 对象
            questions = []
            for q_data in questions_data:
                question = QuestionV2(
                    exam_id=exam_id,
                    subject=subject,
                    content=q_data.get("content"),
                    standard_answer=q_data.get("standard_answer"),
                    question_type=q_data.get("question_type"),
                    position=q_data.get("position"),
                    first_attempt=FirstAttempt(
                        student_answer=q_data.get("student_answer"),
                        is_correct=q_data.get("is_correct", False),
                        teacher_mark=q_data.get("teacher_mark"),
                        deducted_points=q_data.get("deducted_points")
                    )
                )
                questions.append(question)

            return questions

        except Exception as e:
            print(f"警告：解析批阅卷 {image_path.name} 时出错: {e}")
            return []

    def parse_correction_page(
        self,
        image_path: Path,
        original_questions: List[QuestionV2]
    ) -> List[QuestionV2]:
        """
        解析订正页，更新题目的订正状态

        Args:
            image_path: 订正页图片路径
            original_questions: 原始题目列表

        Returns:
            更新后的题目列表
        """
        prompt = """请分析这张订正页，提取学生的订正答案。

对每道订正题，请识别：
1. **题目位置**：第几题
2. **订正答案**：学生订正后的答案
3. **是否正确**：订正答案是否正确

请以 JSON 数组格式返回：
[
  {
    "position": "第5题",
    "corrected_answer": "100",
    "is_correct": true
  },
  ...
]

只返回 JSON 数组，不要包含其他文本。"""

        try:
            # 使用 AI 分析图像
            response_text = self.ai_provider.analyze_image(
                image_path=image_path,
                prompt=prompt
            )

            # 解析 JSON
            response_text = self._clean_json_response(response_text)
            corrections_data = json.loads(response_text)

            # 更新原始题目的订正状态
            for corr_data in corrections_data:
                position = corr_data.get("position")
                # 查找对应的题目
                for question in original_questions:
                    if question.position == position:
                        question.correction = Correction(
                            student_answer=corr_data.get("corrected_answer"),
                            is_correct=corr_data.get("is_correct", False),
                            corrected_at=datetime.now().isoformat(),
                            has_corrected=True
                        )
                        break

            return original_questions

        except Exception as e:
            print(f"警告：解析订正页 {image_path.name} 时出错: {e}")
            return original_questions

    def map_knowledge_points(
        self,
        question: QuestionV2,
        knowledge_graph
    ) -> QuestionV2:
        """
        为题目映射知识点

        Args:
            question: 题目对象
            knowledge_graph: 知识图谱

        Returns:
            更新后的题目对象
        """
        if not question.content:
            return question

        prompt = f"""请分析这道{question.subject}题目，识别它考查的知识点。

题目：{question.content}
题型：{question.question_type}

请从以下角度分析：
1. 这道题主要考查哪些知识点？
2. 难度等级（1-5）？
3. 常见的错误原因有哪些？

请以 JSON 格式返回：
{{
  "knowledge_points": ["知识点1", "知识点2"],
  "difficulty": 3,
  "common_errors": ["错误原因1", "错误原因2"]
}}

只返回 JSON，不要包含其他文本。"""

        try:
            response_text = self.ai_provider.text_completion(
                prompt=prompt,
                temperature=0.3
            )

            # 解析 JSON
            response_text = self._clean_json_response(response_text)
            result = json.loads(response_text)

            # 更新题目信息
            question.knowledge_points = result.get("knowledge_points", [])
            question.difficulty = result.get("difficulty", 3)

            return question

        except Exception as e:
            print(f"警告：知识点映射失败: {e}")
            return question

    def analyze_errors(self, question: QuestionV2) -> QuestionV2:
        """
        分析错误原因和订正质量

        Args:
            question: 题目对象

        Returns:
            更新后的题目对象
        """
        # 如果首次答对了，不需要分析
        if question.first_attempt.is_correct:
            return question

        prompt = f"""请分析这道题目的错误情况：

题目：{question.content}
标准答案：{question.standard_answer}
学生首次答案：{question.first_attempt.student_answer}
学生订正答案：{question.correction.student_answer if question.correction.has_corrected else "未订正"}
订正是否正确：{question.correction.is_correct if question.correction.has_corrected else "N/A"}

请分析：
1. **首次错误原因**：学生为什么答错？（计算错误、理解错误、粗心等）
2. **订正质量**：订正后是否真正理解？
3. **是否需要专项练习**：true/false

请以 JSON 格式返回：
{{
  "first_attempt_reason": "乘法口诀不熟练，计算错误",
  "correction_quality": "订正正确，理解了错误原因",
  "suggest_practice": true
}}

只返回 JSON，不要包含其他文本。"""

        try:
            response_text = self.ai_provider.text_completion(
                prompt=prompt,
                temperature=0.3
            )

            # 解析 JSON
            response_text = self._clean_json_response(response_text)
            result = json.loads(response_text)

            # 更新错误分析
            question.error_analysis = ErrorAnalysis(
                first_attempt_reason=result.get("first_attempt_reason"),
                correction_quality=result.get("correction_quality"),
                suggest_practice=result.get("suggest_practice", False)
            )

            return question

        except Exception as e:
            print(f"警告：错误分析失败: {e}")
            return question

    def _clean_json_response(self, text: str) -> str:
        """清理 AI 返回的 JSON 响应"""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def save_questions(self, questions: List[QuestionV2], output_file: Path) -> None:
        """保存题目数据"""
        data = {
            "total_questions": len(questions),
            "updated_at": datetime.now().isoformat(),
            "questions": [asdict(q) for q in questions]
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_questions(self, input_file: Path) -> List[QuestionV2]:
        """加载题目数据"""
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        questions = []
        for q_data in data["questions"]:
            # 重建嵌套对象
            first_attempt = FirstAttempt(**q_data.get("first_attempt", {}))
            correction = Correction(**q_data.get("correction", {}))
            error_analysis = ErrorAnalysis(**q_data.get("error_analysis", {}))

            question = QuestionV2(
                question_id=q_data.get("question_id"),
                exam_id=q_data.get("exam_id"),
                subject=q_data.get("subject"),
                content=q_data.get("content"),
                standard_answer=q_data.get("standard_answer"),
                first_attempt=first_attempt,
                correction=correction,
                knowledge_points=q_data.get("knowledge_points", []),
                difficulty=q_data.get("difficulty", 3),
                question_type=q_data.get("question_type"),
                page_number=q_data.get("page_number"),
                position=q_data.get("position"),
                error_analysis=error_analysis
            )
            questions.append(question)

        return questions
