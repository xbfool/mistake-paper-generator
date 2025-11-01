"""
竖式计算题生成器
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
class VerticalQuestion:
    """竖式计算题数据类"""
    operation: str  # 运算类型
    numbers: Tuple  # 运算的数字（加减乘: 2个，除法: 4个包含商和余数）
    answer: str  # 答案
    show_work: bool = False  # 是否显示计算过程


class VerticalQuestionGenerator:
    """竖式计算题生成器"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化竖式题生成器

        Args:
            config: 配置字典
        """
        self.config = config or {}

    def generate_batch(self,
                      count: int,
                      operations: List[str] = None,
                      digit_configs: Dict[str, List[str]] = None) -> List[VerticalQuestion]:
        """
        批量生成竖式题

        Args:
            count: 生成数量
            operations: 运算类型列表
            digit_configs: 位数配置

        Returns:
            竖式题列表
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

    def _generate_single(self, operation: str, digit_patterns: List[str]) -> VerticalQuestion:
        """生成单道竖式题"""
        if not digit_patterns:
            digit_patterns = ['2x2']

        pattern = random.choice(digit_patterns)
        a_digits, b_digits = self._parse_pattern(pattern)

        if operation == 'add':
            a, b, result = AdditionGenerator.generate(a_digits, b_digits)
            return VerticalQuestion(
                operation='add',
                numbers=(a, b),
                answer=str(result)
            )

        elif operation == 'sub':
            a, b, result = SubtractionGenerator.generate(a_digits, b_digits)
            return VerticalQuestion(
                operation='sub',
                numbers=(a, b),
                answer=str(result)
            )

        elif operation == 'mul':
            a, b, result = MultiplicationGenerator.generate(a_digits, b_digits)
            return VerticalQuestion(
                operation='mul',
                numbers=(a, b),
                answer=str(result)
            )

        elif operation == 'div':
            dividend, divisor, quotient, remainder = DivisionGenerator.generate(a_digits, b_digits)
            return VerticalQuestion(
                operation='div',
                numbers=(dividend, divisor, quotient, remainder),
                answer=f"{quotient}" + (f"...{remainder}" if remainder > 0 else "")
            )

        else:
            raise ValueError(f"不支持的运算类型: {operation}")

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
            'add': ['3x3', '3x2', '4x3'],
            'sub': ['3x3', '3x2', '4x3'],
            'mul': ['2x2', '3x1', '3x2'],
            'div': ['3x1', '4x1', '4x2']
        }
