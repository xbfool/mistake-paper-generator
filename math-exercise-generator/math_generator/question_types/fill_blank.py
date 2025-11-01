"""
填空题生成器
"""
import random
from typing import List, Tuple, Dict, Any
from dataclasses import dataclass
from ..operations import (
    AdditionGenerator,
    SubtractionGenerator,
    MultiplicationGenerator,
    DivisionGenerator
)


@dataclass
class FillBlankQuestion:
    """填空题数据类"""
    question: str  # 题目文本，如 "( ) + 23 = 45"
    answer: str  # 答案（填空部分）
    operation: str  # 运算类型


class FillBlankGenerator:
    """填空题生成器"""

    def __init__(self, config: Dict[str, Any] = None):
        """初始化填空题生成器"""
        self.config = config or {}

    def generate_batch(self,
                      count: int,
                      operations: List[str] = None,
                      digit_configs: Dict[str, List[str]] = None) -> List[FillBlankQuestion]:
        """
        批量生成填空题

        Args:
            count: 生成数量
            operations: 运算类型列表
            digit_configs: 位数配置

        Returns:
            填空题列表
        """
        if operations is None:
            operations = ['add', 'sub', 'mul', 'div']

        if digit_configs is None:
            digit_configs = self._get_default_configs()

        questions = []

        for i in range(count):
            op = random.choice(operations)
            question = self._generate_single(op, digit_configs.get(op, []))
            questions.append(question)

        return questions

    def _generate_single(self, operation: str, digit_patterns: List[str]) -> FillBlankQuestion:
        """生成单道填空题"""
        if not digit_patterns:
            digit_patterns = ['2x2']

        pattern = random.choice(digit_patterns)
        a_digits, b_digits = self._parse_pattern(pattern)

        # 随机决定哪个位置留空（左边、右边或结果）
        blank_position = random.choice(['left', 'right', 'result'])

        if operation == 'add':
            a, b, result = AdditionGenerator.generate(a_digits, b_digits)

            if blank_position == 'left':
                question_text = f"(      ) + {b} = {result}"
                answer = str(a)
            elif blank_position == 'right':
                question_text = f"{a} + (      ) = {result}"
                answer = str(b)
            else:  # result
                question_text = f"{a} + {b} = (      )"
                answer = str(result)

        elif operation == 'sub':
            a, b, result = SubtractionGenerator.generate(a_digits, b_digits)

            if blank_position == 'left':
                question_text = f"(      ) - {b} = {result}"
                answer = str(a)
            elif blank_position == 'right':
                question_text = f"{a} - (      ) = {result}"
                answer = str(b)
            else:  # result
                question_text = f"{a} - {b} = (      )"
                answer = str(result)

        elif operation == 'mul':
            a, b, result = MultiplicationGenerator.generate(a_digits, b_digits)

            if blank_position == 'left':
                question_text = f"(      ) × {b} = {result}"
                answer = str(a)
            elif blank_position == 'right':
                question_text = f"{a} × (      ) = {result}"
                answer = str(b)
            else:  # result
                question_text = f"{a} × {b} = (      )"
                answer = str(result)

        elif operation == 'div':
            dividend, divisor, quotient, remainder = DivisionGenerator.generate_exact_division(a_digits, b_digits)

            # 除法只在左边或右边留空，结果不留空（太复杂）
            blank_pos = random.choice(['left', 'right'])

            if blank_pos == 'left':
                question_text = f"(      ) ÷ {divisor} = {quotient}"
                answer = str(dividend)
            else:
                question_text = f"{dividend} ÷ (      ) = {quotient}"
                answer = str(divisor)

        else:
            raise ValueError(f"不支持的运算类型: {operation}")

        return FillBlankQuestion(
            question=question_text,
            answer=answer,
            operation=operation
        )

    @staticmethod
    def _parse_pattern(pattern: str) -> Tuple[int, int]:
        """解析位数模式"""
        parts = pattern.lower().split('x')
        if len(parts) != 2:
            raise ValueError(f"无效的位数模式: {pattern}")
        return int(parts[0]), int(parts[1])

    @staticmethod
    def _get_default_configs() -> Dict[str, List[str]]:
        """获取默认配置"""
        return {
            'add': ['2x2', '3x2', '3x3'],
            'sub': ['2x2', '3x2', '3x3'],
            'mul': ['2x1', '2x2'],
            'div': ['2x1', '3x1']
        }
