"""
口算题生成器
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
class OralQuestion:
    """口算题数据类"""
    question: str  # 题目文本，如 "23 + 45 = ___"
    answer: str  # 答案
    operation: str  # 运算类型：add/sub/mul/div


class OralQuestionGenerator:
    """口算题生成器"""

    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化口算题生成器

        Args:
            config: 配置字典，包含运算类型和位数配置
        """
        self.config = config or {}

    def generate_batch(self,
                      count: int,
                      operations: List[str] = None,
                      digit_configs: Dict[str, List[str]] = None) -> List[OralQuestion]:
        """
        批量生成口算题

        Args:
            count: 生成数量
            operations: 包含的运算类型列表 ['add', 'sub', 'mul', 'div']
            digit_configs: 每种运算的位数配置
                          格式: {'add': ['2x2', '3x2'], 'mul': ['2x1']}

        Returns:
            口算题列表
        """
        if operations is None:
            operations = ['add', 'sub', 'mul', 'div']

        if digit_configs is None:
            digit_configs = self._get_default_configs()

        questions = []

        for i in range(count):
            # 随机选择运算类型
            op = random.choice(operations)

            # 生成题目
            question = self._generate_single(op, digit_configs.get(op, []))
            questions.append(question)

        return questions

    def _generate_single(self, operation: str, digit_patterns: List[str]) -> OralQuestion:
        """
        生成单道口算题

        Args:
            operation: 运算类型
            digit_patterns: 位数模式列表，如 ['2x2', '3x1']

        Returns:
            口算题对象
        """
        if not digit_patterns:
            digit_patterns = ['2x2']

        # 随机选择位数模式
        pattern = random.choice(digit_patterns)
        a_digits, b_digits = self._parse_pattern(pattern)

        if operation == 'add':
            a, b, result = AdditionGenerator.generate(a_digits, b_digits)
            question_text = f"{a} + {b} ="
            answer = str(result)

        elif operation == 'sub':
            a, b, result = SubtractionGenerator.generate(a_digits, b_digits)
            question_text = f"{a} - {b} ="
            answer = str(result)

        elif operation == 'mul':
            a, b, result = MultiplicationGenerator.generate(a_digits, b_digits)
            question_text = f"{a} × {b} ="
            answer = str(result)

        elif operation == 'div':
            dividend, divisor, quotient, remainder = DivisionGenerator.generate(a_digits, b_digits)
            if remainder == 0:
                question_text = f"{dividend} ÷ {divisor} ="
                answer = str(quotient)
            else:
                question_text = f"{dividend} ÷ {divisor} ="
                answer = f"{quotient}...{remainder}"

        else:
            raise ValueError(f"不支持的运算类型: {operation}")

        return OralQuestion(
            question=question_text,
            answer=answer,
            operation=operation
        )

    @staticmethod
    def _parse_pattern(pattern: str) -> Tuple[int, int]:
        """
        解析位数模式

        Args:
            pattern: 如 "3x2" 表示 3位数 × 2位数

        Returns:
            (a_digits, b_digits) 元组
        """
        parts = pattern.lower().split('x')
        if len(parts) != 2:
            raise ValueError(f"无效的位数模式: {pattern}")

        return int(parts[0]), int(parts[1])

    @staticmethod
    def _get_default_configs() -> Dict[str, List[str]]:
        """获取默认的位数配置（三年级水平）"""
        return {
            'add': ['2x2', '3x2', '3x3'],
            'sub': ['2x2', '3x2', '3x3'],
            'mul': ['2x1', '2x2', '3x1'],
            'div': ['2x1', '3x1']
        }
