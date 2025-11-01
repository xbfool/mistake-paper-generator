"""
乘法生成器
"""
import random
from typing import Tuple, Optional
from ..number_gen import NumberGenerator


class MultiplicationGenerator:
    """乘法题目生成器"""

    @staticmethod
    def generate(a_digits: int,
                 b_digits: int,
                 max_result: int = 9999,
                 round_to: Optional[int] = None,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None) -> Tuple[int, int, int]:
        """
        生成乘法题

        Args:
            a_digits: 被乘数的位数 (1-4)
            b_digits: 乘数的位数 (1-4)
            max_result: 结果的最大值（默认9999，即4位数）
            round_to: 结果取整到
            min_val: 最小值
            max_val: 最大值

        Returns:
            (multiplicand, multiplier, result) 元组
        """
        max_attempts = 100
        for _ in range(max_attempts):
            multiplicand = NumberGenerator.generate(a_digits, min_val, max_val)
            multiplier = NumberGenerator.generate(b_digits, min_val, max_val)

            result = multiplicand * multiplier

            # 检查结果是否超过最大值
            if result > max_result:
                continue

            # 检查取整要求
            if round_to and result % round_to != 0:
                continue

            return multiplicand, multiplier, result

        # 如果100次都没生成合适的，降低被乘数范围
        multiplicand = NumberGenerator.generate(a_digits, min_val=1, max_val=min(99, max_val or 99))
        multiplier = NumberGenerator.generate(b_digits, min_val=1, max_val=min(99, max_val or 99))

        result = multiplicand * multiplier

        # 确保结果不超过max_result
        while result > max_result:
            multiplicand = multiplicand // 2
            if multiplicand < 1:
                multiplicand = 1
            result = multiplicand * multiplier

        return multiplicand, multiplier, result

    @staticmethod
    def generate_table(a_digit: int, b_digit: int) -> Tuple[int, int, int]:
        """
        生成乘法口诀表内的题目（1-9）

        Args:
            a_digit: 第一个数（1-9）
            b_digit: 第二个数（1-9）

        Returns:
            (a, b, result) 元组
        """
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return a, b, a * b

    @staticmethod
    def generate_round_result(a_digits: int,
                              b_digits: int,
                              round_to: int) -> Tuple[int, int, int]:
        """
        生成结果为整十、整百的乘法题

        Args:
            a_digits: 被乘数位数
            b_digits: 乘数位数
            round_to: 取整到（10/100/1000）

        Returns:
            (a, b, result) 元组
        """
        return MultiplicationGenerator.generate(
            a_digits,
            b_digits,
            round_to=round_to
        )
