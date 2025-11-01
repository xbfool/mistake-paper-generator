"""
除法生成器
"""
import random
from typing import Tuple, Optional
from ..number_gen import NumberGenerator


class DivisionGenerator:
    """除法题目生成器"""

    @staticmethod
    def generate(dividend_digits: int,
                 divisor_digits: int,
                 allow_remainder: bool = True,
                 force_remainder: bool = False,
                 min_val: Optional[int] = None,
                 max_val: Optional[int] = None) -> Tuple[int, int, int, int]:
        """
        生成除法题

        Args:
            dividend_digits: 被除数的位数 (1-4)
            divisor_digits: 除数的位数 (1-3)
            allow_remainder: 允许有余数
            force_remainder: 强制有余数
            min_val: 最小值
            max_val: 最大值

        Returns:
            (dividend, divisor, quotient, remainder) 元组
        """
        if divisor_digits > 3:
            raise ValueError("除数最多3位")

        if force_remainder and not allow_remainder:
            raise ValueError("force_remainder 和 allow_remainder=False 冲突")

        max_attempts = 100
        for _ in range(max_attempts):
            if not allow_remainder:
                # 整除：先生成除数和商，再计算被除数
                divisor = NumberGenerator.generate(divisor_digits, min_val=2, max_val=max_val)
                quotient_digits = max(1, dividend_digits - divisor_digits + 1)
                quotient = NumberGenerator.generate(quotient_digits)
                dividend = divisor * quotient
                remainder = 0

                # 检查被除数位数是否符合要求
                if len(str(dividend)) != dividend_digits:
                    continue

                return dividend, divisor, quotient, remainder

            elif force_remainder:
                # 强制有余数
                divisor = NumberGenerator.generate(divisor_digits, min_val=2, max_val=max_val)
                quotient_digits = max(1, dividend_digits - divisor_digits)
                quotient = NumberGenerator.generate(quotient_digits)
                remainder = random.randint(1, divisor - 1)
                dividend = divisor * quotient + remainder

                # 检查被除数位数是否符合要求
                if len(str(dividend)) != dividend_digits:
                    continue

                return dividend, divisor, quotient, remainder

            else:
                # 随机
                dividend = NumberGenerator.generate(dividend_digits, min_val, max_val)
                divisor = NumberGenerator.generate(divisor_digits, min_val=2, max_val=max_val)

                # 确保除数不为0且小于被除数
                if divisor >= dividend:
                    continue

                quotient, remainder = divmod(dividend, divisor)

                return dividend, divisor, quotient, remainder

        # 如果100次都没成功，生成一个基本的
        divisor = NumberGenerator.generate(divisor_digits, min_val=2)
        quotient = NumberGenerator.generate(max(1, dividend_digits - divisor_digits))
        remainder = 0 if not force_remainder else random.randint(1, divisor - 1)
        dividend = divisor * quotient + remainder

        return dividend, divisor, quotient, remainder

    @staticmethod
    def generate_exact_division(dividend_digits: int,
                                divisor_digits: int) -> Tuple[int, int, int, int]:
        """
        生成整除的除法题

        Args:
            dividend_digits: 被除数位数
            divisor_digits: 除数位数

        Returns:
            (dividend, divisor, quotient, 0) 元组
        """
        return DivisionGenerator.generate(
            dividend_digits,
            divisor_digits,
            allow_remainder=False
        )

    @staticmethod
    def generate_with_remainder(dividend_digits: int,
                                divisor_digits: int) -> Tuple[int, int, int, int]:
        """
        生成有余数的除法题

        Args:
            dividend_digits: 被除数位数
            divisor_digits: 除数位数

        Returns:
            (dividend, divisor, quotient, remainder) 元组
        """
        return DivisionGenerator.generate(
            dividend_digits,
            divisor_digits,
            force_remainder=True
        )
