"""Численное решение нелинейного уравнения для оценки B (п. «а» задания).

sum_{i=1..n} 1/(B-i+1) = n * sum(Xi) / ((B+1) * sum(Xi) - sum(i*Xi))
"""

from collections.abc import Callable

# Правая граница поиска B, в которой считаем, что конечной оценки нет
MAX_B = 1e6


def find_root(
    func: Callable[[float], float],
    left: float,
    right: float,
    eps: float = 1e-6,
    max_iter: int = 1000,
) -> float:
    """Найти корень func на отрезке [left, right] методом половинного деления.

    На концах отрезка функция должна иметь разные знаки.
    """
    f_left = func(left)
    if f_left * func(right) > 0:
        raise ValueError("На концах отрезка функция имеет одинаковый знак")

    for _ in range(max_iter):
        middle = (left + right) / 2
        f_middle = func(middle)
        if f_middle == 0 or right - left < eps:
            return middle
        if f_left * f_middle < 0:
            right = middle
        else:
            left, f_left = middle, f_middle
    return (left + right) / 2


def b_equation(intervals: list[float]) -> Callable[[float], float]:
    """Функция f(B) = левая часть - правая часть уравнения; её корень — оценка B."""
    n = len(intervals)
    total = sum(intervals)
    weighted = sum(i * x for i, x in enumerate(intervals, start=1))

    def f(b: float) -> float:
        left_side = sum(1 / (b - i + 1) for i in range(1, n + 1))
        right_side = n * total / ((b + 1) * total - weighted)
        return left_side - right_side

    return f


def estimate_b(intervals: list[float]) -> float:
    """Оценка максимального правдоподобия общего числа ошибок B.

    Корень ищется при B > n - 1: около n - 1 функция f(B) положительна,
    а при больших B становится отрицательной, только если интервалы между
    ошибками в среднем растут (sum(i*Xi) / sum(Xi) > (n+1)/2). Иначе модель
    неприменима — оценка B уходит в бесконечность.
    """
    n = len(intervals)
    if n < 2:
        raise ValueError("Нужно хотя бы два интервала между ошибками")
    if any(x <= 0 for x in intervals):
        raise ValueError("Интервалы между ошибками должны быть положительными")

    total = sum(intervals)
    weighted = sum(i * x for i, x in enumerate(intervals, start=1))
    if weighted / total <= (n + 1) / 2:
        raise ValueError(
            "Интервалы между ошибками не растут — надёжность не повышается, "
            "модель Джелинского-Моранды не даёт конечной оценки B"
        )

    f = b_equation(intervals)
    left = n - 1 + 1e-9
    right = float(n)
    while f(right) > 0:
        right *= 2
        if right > MAX_B:
            raise ValueError("Не удалось найти оценку B: корень слишком велик")
    return find_root(f, left, right, eps=1e-9)
