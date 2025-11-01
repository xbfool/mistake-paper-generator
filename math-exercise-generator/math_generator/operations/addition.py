"""
加法生成器
"""
import random
from typing import Tuple, Optional
from ..number_gen import NumberGenerator


class AdditionGenerator:
    """加法题目生成器"""

    @staticmethod
    def generate(a_digits: int,
                 b_digits: int,
                 force_carry: bool = False,
                 no_carry: bool = False,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None) -> Tuple[int, int, int]:
        """
        生成加法题

        Args:
            a_digits: 第一个加数的位数 (1-4)
            b_digits: 第二个加数的位数 (1-4)
            force_carry: 强制进位
            no_carry: 禁止进位
            min_val: 最小值
            max_val: 最大值

        Returns:
            (a, b, result) 元组
        """
        if force_carry and no_carry:
            raise ValueError("force_carry 和 no_carry 不能同时为 True")

        max_attempts = 100
        for _ in range(max_attempts):
            a = NumberGenerator.generate(a_digits, min_val, max_val)
            b = NumberGenerator.generate(b_digits, min_val, max_val)

            result = a + b

            # 检查是否需要进位
            has_carry = AdditionGenerator._check_carry(a, b)

            if force_carry and not has_carry:
                continue
            if no_carry and has_carry:
                continue

            return a, b, result

        # 如果100次都没生成合适的，放宽限制
        a = NumberGenerator.generate(a_digits, min_val, max_val)
        b = NumberGenerator.generate(b_digits, min_val, max_val)
        return a, b, a + b

    @staticmethod
    def _check_carry(a: int, b: int) -> bool:
        """
        检查加法是否需要进位

        Args:
            a: 第一个加数
            b: 第二个加数

        Returns:
            是否需要进位
        """
        a_str = str(a)
        b_str = str(b)

        # 对齐到相同长度
        max_len = max(len(a_str), len(b_str))
        a_str = a_str.zfill(max_len)
        b_str = b_str.zfill(max_len)

        # 从右往左检查每一位
        for i in range(max_len - 1, -1, -1):
            digit_sum = int(a_str[i]) + int(b_str[i])
            if digit_sum >= 10:
                return True

        return False

    @staticmethod
    def generate_carry_addition(a_digits: int, b_digits: int) -> Tuple[int, int, int]:
        """生成一定进位的加法题"""
        return AdditionGenerator.generate(a_digits, b_digits, force_carry=True)

    @staticmethod
    def generate_no_carry_addition(a_digits: int, b_digits: int) -> Tuple[int, int, int]:
        """生成不进位的加法题"""
        return AdditionGenerator.generate(a_digits, b_digits, no_carry=True)
