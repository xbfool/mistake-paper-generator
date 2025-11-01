"""
数字生成器
支持1-4位数的灵活生成
"""
import random
from typing import Optional


class NumberGenerator:
    """数字生成器类"""

    @staticmethod
    def generate(digits: int,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None,
                 round_to: Optional[int] = None) -> int:
        """
        生成指定位数的数字

        Args:
            digits: 位数 (1-4)
            min_val: 最小值
            max_val: 最大值
            round_to: 取整到（10/100/1000）

        Returns:
            生成的数字
        """
        if digits < 1 or digits > 4:
            raise ValueError("位数必须在1-4之间")

        # 确定范围
        if min_val is None:
            min_val = 10 ** (digits - 1) if digits > 1 else 1
        if max_val is None:
            max_val = 10 ** digits - 1

        # 生成随机数
        num = random.randint(min_val, max_val)

        # 取整
        if round_to and round_to > 1:
            num = (num // round_to) * round_to
            # 确保不为0
            if num == 0:
                num = round_to

        return num

    @staticmethod
    def generate_with_constraint(digits: int,
                                 avoid_zero: bool = True,
                                 **kwargs) -> int:
        """
        生成带约束的数字

        Args:
            digits: 位数
            avoid_zero: 避免生成0
            **kwargs: 其他参数传递给generate

        Returns:
            生成的数字
        """
        num = NumberGenerator.generate(digits, **kwargs)

        # 避免0
        if avoid_zero and num == 0:
            num = NumberGenerator.generate(digits, **kwargs)

        return num
