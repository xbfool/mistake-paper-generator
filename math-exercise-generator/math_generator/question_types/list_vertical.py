"""
列竖式计算题生成器
给出横式，要求学生列竖式计算
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
class ListVerticalQuestion:
    """列竖式计算题数据类"""
    question: str  # 题目文本，如 "456 + 234 = ___（请列竖式计算）"
    answer: str  # 答案
    operation: str  # 运算类型
    numbers: Tuple  # 运算的数字


class ListVerticalGenerator:
    """列竖式计算题生成器"""

    def __init__(self, config: Dict[str, Any] = None):
        """初始化列竖式生成器"""
        self.config = config or {}

    def generate_batch(self,
                      count: int,
                      operations: List[str] = None,
                      digit_configs: Dict[str, List[str]] = None) -> List[ListVerticalQuestion]:
        """
        批量生成列竖式题

        Args:
            count: 生成数量
            operations: 运算类型列表
            digit_configs: 位数配置

        Returns:
            列竖式题列表
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

    def _generate_single(self, operation: str, digit_patterns: List[str]) -> ListVerticalQuestion:
        """生成单道列竖式题"""
        if not digit_patterns:
            digit_patterns = ['3x3']

        pattern = random.choice(digit_patterns)
        a_digits, b_digits = self._parse_pattern(pattern)

        if operation == 'add':
            a, b, result = AdditionGenerator.generate(a_digits, b_digits)
            question_text = f"{a} + {b} = ___"
            answer = str(result)
            numbers = (a, b, result)

        elif operation == 'sub':
            a, b, result = SubtractionGenerator.generate(a_digits, b_digits)
            question_text = f"{a} - {b} = ___"
            answer = str(result)
            numbers = (a, b, result)

        elif operation == 'mul':
            a, b, result = MultiplicationGenerator.generate(a_digits, b_digits)
            question_text = f"{a} × {b} = ___"
            answer = str(result)
            numbers = (a, b, result)

        elif operation == 'div':
            dividend, divisor, quotient, remainder = DivisionGenerator.generate(a_digits, b_digits)
            if remainder == 0:
                question_text = f"{dividend} ÷ {divisor} = ___"
                answer = str(quotient)
            else:
                question_text = f"{dividend} ÷ {divisor} = ___ ... ___"
                answer = f"{quotient}...{remainder}"
            numbers = (dividend, divisor, quotient, remainder)

        else:
            raise ValueError(f"不支持的运算类型: {operation}")

        return ListVerticalQuestion(
            question=question_text,
            answer=answer,
            operation=operation,
            numbers=numbers
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
            'add': ['3x3', '4x3', '4x4'],
            'sub': ['3x3', '4x3', '4x4'],
            'mul': ['2x2', '3x2'],
            'div': ['3x1', '4x2']
        }
