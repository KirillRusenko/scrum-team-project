"""Численное решение нелинейного уравнения для оценки B (п. «а» задания).

sum_{i=1..n} 1/(B-i+1) = n * sum(Xi) / ((B+1) * sum(Xi) - sum(i*Xi))
"""

from collections.abc import Callable


def find_root(
    func: Callable[[float], float],
    left: float,
    right: float,
    eps: float = 1e-6,
    max_iter: int = 1000,
) -> float:
    """Найти корень func на отрезке [left, right] (например, методом половинного деления)."""
    raise NotImplementedError


def estimate_b(intervals: list[float]) -> float:
    """Оценка максимального правдоподобия общего числа ошибок B."""
    raise NotImplementedError
