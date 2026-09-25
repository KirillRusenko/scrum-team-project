"""Расчётные формулы модели Джелинского-Моранды (пп. «б»–«г» задания)."""

import math
from dataclasses import dataclass

from jelinski_moranda.solver import estimate_b


@dataclass
class ModelResult:
    n: int  # число обнаруженных ошибок
    b: float  # общее число ошибок в программе
    k: float  # коэффициент пропорциональности
    next_error_time: float  # X(n+1) — среднее время до следующей ошибки, ч
    time_to_end: float  # t_k — время до окончания тестирования, ч

    @property
    def remaining_errors(self) -> int:
        """Число оставшихся в программе ошибок B - n (округлённое до целого)."""
        return remaining_errors(self.n, self.b)


def remaining_errors(n: int, b: float) -> int:
    """Число оставшихся ошибок B - n, округлённое до целого (не меньше 0)."""
    return max(round(b - n), 0)


def coefficient_k(intervals: list[float], b: float) -> float:
    """K = n / ((B+1) * sum(Xi) - sum(i*Xi))."""
    n = len(intervals)
    total = sum(intervals)
    weighted = sum(i * x for i, x in enumerate(intervals, start=1))
    return n / ((b + 1) * total - weighted)


def next_error_time(n: int, b: float, k: float) -> float:
    """X(n+1) = 1 / (K * (B - n)).

    Если B <= n, все ошибки уже найдены и следующей не ожидается — возвращается inf.
    """
    if b <= n:
        return math.inf
    return 1 / (k * (b - n))


def time_to_end(n: int, b: float, k: float) -> float:
    """t_k = (1/K) * sum_{i=1..B-n} 1/i."""
    return sum(1 / i for i in range(1, remaining_errors(n, b) + 1)) / k


def calculate(intervals: list[float]) -> ModelResult:
    """Полный расчёт модели по интервалам между ошибками."""
    n = len(intervals)
    b = estimate_b(intervals)
    k = coefficient_k(intervals, b)
    return ModelResult(
        n=n,
        b=b,
        k=k,
        next_error_time=next_error_time(n, b, k),
        time_to_end=time_to_end(n, b, k),
    )
