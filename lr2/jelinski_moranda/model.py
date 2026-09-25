"""Расчётные формулы модели Джелинского-Моранды (пп. «б»–«г» задания)."""

from dataclasses import dataclass


@dataclass
class ModelResult:
    n: int  # число обнаруженных ошибок
    b: float  # общее число ошибок в программе
    k: float  # коэффициент пропорциональности
    next_error_time: float  # X(n+1) — среднее время до следующей ошибки, ч
    time_to_end: float  # t_k — время до окончания тестирования, ч


def coefficient_k(intervals: list[float], b: float) -> float:
    """K = n / ((B+1) * sum(Xi) - sum(i*Xi))."""
    raise NotImplementedError


def next_error_time(n: int, b: float, k: float) -> float:
    """X(n+1) = 1 / (K * (B - n))."""
    raise NotImplementedError


def time_to_end(n: int, b: float, k: float) -> float:
    """t_k = (1/K) * sum_{i=1..B-n} 1/i."""
    raise NotImplementedError


def calculate(intervals: list[float]) -> ModelResult:
    """Полный расчёт модели по интервалам между ошибками."""
    raise NotImplementedError
