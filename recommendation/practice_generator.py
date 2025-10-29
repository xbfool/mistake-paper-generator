"""
练习题生成系统
根据推荐方案生成练习题
"""
import os
import json
from typing import Dict, List
from anthropic import Anthropic
from knowledge_system.knowledge_base import KnowledgePoint


class PracticeGenerator:
    """练习题生成器"""

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate_practice_by_plan(
        self,
        plan: Dict,
        knowledge_graph
    ) -> List[Dict]:
        """
        根据推荐方案生成练习题

        Args:
            plan: 推荐方案
            knowledge_graph: 知识图谱

        Returns:
            练习题列表
        """
        print(f"\n根据方案「{plan['name']}」生成练习题...")
        print("="*60)

        questions = []

        # 获取知识点列表
        knowledge_points_data = plan.get("knowledge_points", [])

        if not knowledge_points_data:
            # 如果方案中没有具体知识点，返回通用题目
            return self._generate_general_questions(plan)

        # 为每个知识点生成题目
        for kp_data in knowledge_points_data:
            point_id = kp_data["id"]
            questions_count = kp_data.get("questions_count", 5)

            point = knowledge_graph.get_point(point_id)
            if not point:
                continue

            point_questions = self.generate_questions_for_point(
                point,
                count=questions_count
            )

            questions.extend(point_questions)

        print(f"✓ 共生成 {len(questions)} 道练习题")

        return questions

    def generate_questions_for_point(
        self,
        point: KnowledgePoint,
        count: int = 5,
        difficulty: int = None
    ) -> List[Dict]:
        """
        为某个知识点生成练习题

        Args:
            point: 知识点
            count: 题目数量
            difficulty: 指定难度（None则使用知识点的难度）

        Returns:
            题目列表
        """
        if difficulty is None:
            difficulty = point.difficulty.value

        print(f"  为「{point.name}」生成{count}道题...", end="", flush=True)

        prompt = f"""请为小学{point.grade}年级{point.subject.value}知识点「{point.name}」生成{count}道练习题。

知识点信息：
- 描述：{point.description}
- 难度：{difficulty}/5
- 典型题型：{', '.join(point.typical_questions)}
- 常见错误：{', '.join(point.common_mistakes)}
- 学习建议：{point.learning_tips}

要求：
1. 题目要准确考查该知识点
2. 难度适中，由易到难
3. 题型多样（包括{', '.join(point.typical_questions[:3])}等）
4. 每道题包含：题目内容、正确答案、简要解析

返回JSON格式：
{{
  "questions": [
    {{
      "question_number": 1,
      "question_content": "题目内容",
      "question_type": "题型（如口算题、应用题等）",
      "correct_answer": "正确答案",
      "explanation": "解析（简要）",
      "difficulty": {difficulty},
      "knowledge_point": "{point.name}"
    }}
  ]
}}"""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # 提取JSON
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            result = json.loads(response_text)
            questions = result.get("questions", [])

            # 添加元数据
            for q in questions:
                q["knowledge_point_id"] = point.id
                q["grade"] = point.grade
                q["subject"] = point.subject.value

            print(f" ✓ {len(questions)}题")

            return questions

        except Exception as e:
            print(f" ✗ 失败: {e}")
            return []

    def _generate_general_questions(self, plan: Dict) -> List[Dict]:
        """生成通用题目（当没有具体知识点时）"""
        # 简化实现
        return []


if __name__ == "__main__":
    # 测试
    from pathlib import Path
    from knowledge_system.knowledge_graph import KnowledgeGraph

    graph = KnowledgeGraph(Path("knowledge_data"))
    generator = PracticeGenerator()

    # 测试为某个知识点生成题目
    point = graph.get_point("math_1_addition_10")
    if point:
        questions = generator.generate_questions_for_point(point, count=3)

        print(f"\n生成了 {len(questions)} 道题:")
        for q in questions:
            print(f"\n{q['question_number']}. {q['question_content']}")
            print(f"   答案：{q['correct_answer']}")
