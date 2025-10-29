"""
相似题生成模块
使用 Claude API 基于错题生成相似的练习题
"""
import json
from typing import List, Dict, Any
from anthropic import Anthropic
from .config import ANTHROPIC_API_KEY, CLAUDE_MODEL, SIMILAR_QUESTIONS_COUNT
from .question_bank import Question


class QuestionGenerator:
    """相似题生成器"""

    def __init__(self, api_key: str = None):
        """
        初始化生成器

        Args:
            api_key: Anthropic API密钥，如果不提供则从配置中读取
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("未找到 ANTHROPIC_API_KEY，请在 .env 文件中配置")
        self.client = Anthropic(api_key=self.api_key)

    def generate_similar_questions(
        self,
        original_question: Question,
        count: int = SIMILAR_QUESTIONS_COUNT
    ) -> List[Dict[str, Any]]:
        """
        基于原题生成相似题

        Args:
            original_question: 原题（错题）
            count: 要生成的相似题数量

        Returns:
            相似题列表
        """
        print(f"正在为题目「{original_question.question_number}」生成 {count} 道相似题...")

        # 构建提示词
        prompt = f"""你是一位经验丰富的小学三年级数学老师。请基于以下错题，生成 {count} 道相似的练习题。

原题信息：
- 题目类型：{original_question.question_type}
- 题目内容：{original_question.question_content}
- 知识点：{', '.join(original_question.knowledge_points) if original_question.knowledge_points else '未指定'}
- 学生答案：{original_question.student_answer or '未作答'}
- 正确答案：{original_question.correct_answer or '未知'}
- 错误原因：{original_question.mistake_type or '未分析'}

要求：
1. 生成的题目应该与原题在知识点、难度上相似
2. 但题目内容要有所变化（比如换数字、换场景、换问法等）
3. 每道题目都要确保数学正确性
4. 如果原题是应用题，生成的题目也应该是应用题，但场景可以不同
5. 如果原题是计算题，生成的题目也应该是计算题，但数字要不同
6. 题目难度要适合三年级学生

请以JSON格式返回结果，格式如下：
{{
    "similar_questions": [
        {{
            "question_content": "题目内容（完整的题目文本）",
            "correct_answer": "正确答案",
            "solution": "解题步骤说明（简要）",
            "knowledge_points": ["知识点1", "知识点2"]
        }},
        ...
    ]
}}

注意：
- 请确保生成 {count} 道题目
- 每道题都必须有明确的正确答案
- 请确保返回的是有效的JSON格式
- 数学公式用文本形式表示（如：3×5=15）"""

        try:
            # 调用Claude API
            message = self.client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=2048,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            # 解析响应
            response_text = message.content[0].text.strip()

            # 提取JSON部分
            if "```json" in response_text:
                start = response_text.find("```json") + 7
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()
            elif "```" in response_text:
                start = response_text.find("```") + 3
                end = response_text.find("```", start)
                response_text = response_text[start:end].strip()

            # 解析JSON
            result = json.loads(response_text)
            similar_questions = result.get('similar_questions', [])

            print(f"  成功生成 {len(similar_questions)} 道相似题")
            return similar_questions

        except Exception as e:
            print(f"  生成失败: {str(e)}")
            return []

    def generate_for_mistakes(
        self,
        mistakes: List[Question],
        count_per_question: int = SIMILAR_QUESTIONS_COUNT
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        为多道错题批量生成相似题

        Args:
            mistakes: 错题列表
            count_per_question: 每道错题生成的相似题数量

        Returns:
            字典，键为原题ID，值为相似题列表
        """
        print(f"\n开始为 {len(mistakes)} 道错题生成相似题...")
        print("=" * 60)

        results = {}
        for idx, mistake in enumerate(mistakes, 1):
            print(f"\n[{idx}/{len(mistakes)}] ", end="")
            similar_questions = self.generate_similar_questions(mistake, count_per_question)
            results[mistake.id] = similar_questions

        print("\n" + "=" * 60)
        total_generated = sum(len(v) for v in results.values())
        print(f"生成完成！共生成 {total_generated} 道相似题")

        return results

    def generate_practice_set(
        self,
        mistakes: List[Question],
        include_original: bool = True,
        similar_count: int = SIMILAR_QUESTIONS_COUNT
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        生成练习题集（原题+相似题，按题型分类）

        Args:
            mistakes: 错题列表
            include_original: 是否包含原题
            similar_count: 每道错题生成的相似题数量

        Returns:
            按题型分类的练习题集
        """
        print("\n生成练习题集...")

        # 按题型分组
        mistakes_by_type = {}
        for mistake in mistakes:
            q_type = mistake.question_type
            if q_type not in mistakes_by_type:
                mistakes_by_type[q_type] = []
            mistakes_by_type[q_type].append(mistake)

        # 为每个题型生成练习题
        practice_set = {}
        for q_type, type_mistakes in mistakes_by_type.items():
            print(f"\n处理题型：{q_type} ({len(type_mistakes)} 道错题)")
            practice_set[q_type] = []

            for mistake in type_mistakes:
                section = {
                    "original_question": None,
                    "similar_questions": []
                }

                # 添加原题
                if include_original:
                    section["original_question"] = {
                        "question_number": mistake.question_number,
                        "question_content": mistake.question_content,
                        "student_answer": mistake.student_answer,
                        "correct_answer": mistake.correct_answer,
                        "is_original": True
                    }

                # 生成相似题
                similar_questions = self.generate_similar_questions(mistake, similar_count)
                section["similar_questions"] = similar_questions

                practice_set[q_type].append(section)

        return practice_set


if __name__ == "__main__":
    # 测试代码
    from .config import QUESTION_BANK_PATH
    from .question_bank import QuestionBank

    # 加载题库
    bank = QuestionBank(QUESTION_BANK_PATH)
    mistakes = bank.get_mistakes()

    if not mistakes:
        print("题库中没有错题，请先运行图像分析")
    else:
        # 测试生成相似题
        generator = QuestionGenerator()
        practice_set = generator.generate_practice_set(mistakes[:2], similar_count=2)

        # 打印结果
        for q_type, sections in practice_set.items():
            print(f"\n题型：{q_type}")
            for section in sections:
                if section["original_question"]:
                    print(f"  原题：{section['original_question']['question_content'][:50]}...")
                print(f"  相似题数量：{len(section['similar_questions'])}")
