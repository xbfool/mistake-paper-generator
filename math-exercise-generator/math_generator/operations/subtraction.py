"""
减法生成器
"""
import random
from typing import Tuple, Optional
from ..number_gen import NumberGenerator


class SubtractionGenerator:
    """减法题目生成器"""

    @staticmethod
    def generate(a_digits: int,
                 b_digits: int,
                 force_borrow: bool = False,
                 no_borrow: bool = False,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None) -> Tuple[int, int, int]:
        """
        生成减法题

        Args:
            a_digits: 被减数的位数 (1-4)
            b_digits: 减数的位数 (1-4)
            force_borrow: 强制退位
            no_borrow: 禁止退位
            min_val: 最小值
            max_val: 最大值

        Returns:
            (minuend, subtrahend, result) 元组
        """
        if force_borrow and no_borrow:
            raise ValueError("force_borrow 和 no_borrow 不能同时为 True")

        max_attempts = 100
        for _ in range(max_attempts):
            minuend = NumberGenerator.generate(a_digits, min_val, max_val)
            subtrahend = NumberGenerator.generate(b_digits, min_val, max_val)

            # 确保被减数 > 减数（结果为正数）
            if minuend <= subtrahend:
                continue

            result = minuend - subtrahend

            # 检查是否需要退位
            has_borrow = SubtractionGenerator._check_borrow(minuend, subtrahend)

            if force_borrow and not has_borrow:
                continue
            if no_borrow and has_borrow:
                continue

            return minuend, subtrahend, result

        # 如果100次都没生成合适的，放宽限制
        minuend = NumberGenerator.generate(a_digits, min_val, max_val)
        subtrahend = NumberGenerator.generate(b_digits, min_val, max_val)

        # 确保结果为正
        if minuend <= subtrahend:
            minuend, subtrahend = subtrahend, minuend

        return minuend, subtrahend, minuend - subtrahend

    @staticmethod
    def _check_borrow(minuend: int, subtrahend: int) -> bool:
        """
        检查减法是否需要退位

        Args:
            minuend: 被减数
            subtrahend: 减数

        Returns:
            是否需要退位
        """
        minuend_str = str(minuend)
        subtrahend_str = str(subtrahend)

        # 对齐到相同长度
        max_len = max(len(minuend_str), len(subtrahend_str))
        minuend_str = minuend_str.zfill(max_len)
        subtrahend_str = subtrahend_str.zfill(max_len)

        # 从右往左检查每一位
        for i in range(max_len - 1, -1, -1):
            if int(minuend_str[i]) < int(subtrahend_str[i]):
                return True

        return False

    @staticmethod
    def generate_borrow_subtraction(a_digits: int, b_digits: int) -> Tuple[int, int, int]:
        """生成一定退位的减法题"""
        return SubtractionGenerator.generate(a_digits, b_digits, force_borrow=True)

    @staticmethod
    def generate_no_borrow_subtraction(a_digits: int, b_digits: int) -> Tuple[int, int, int]:
        """生成不退位的减法题"""
        return SubtractionGenerator.generate(a_digits, b_digits, no_borrow=True)
