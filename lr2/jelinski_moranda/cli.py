"""Ввод исходных данных и вывод результатов расчёта."""

import math

from jelinski_moranda.data import INTERVALS
from jelinski_moranda.model import ModelResult, calculate


def parse_intervals(text: str) -> list[float]:
    """Разобрать интервалы из строки: числа через пробел, запятую или точку с запятой."""
    parts = text.replace(";", " ").replace(",", " ").split()
    return [float(p) for p in parts]


def read_intervals() -> list[float]:
    """Получить интервалы Xi: данные из задания (data.py) или ручной ввод.

    Если ввода нет (например, запуск в Docker без -it), берутся данные из задания.
    """
    print("Исходные данные:")
    print("  1 — интервалы из задания (вариант 1)")
    print("  2 — ввести интервалы вручную")
    try:
        choice = input("Выбор [1]: ").strip()
        if choice != "2":
            return list(INTERVALS)
        while True:
            text = input("Интервалы Xi в часах через пробел: ")
            try:
                return parse_intervals(text)
            except ValueError:
                print("Ошибка: вводите только числа, например: 9 12 11 4")
    except EOFError:
        print("\nВвод недоступен — используются данные из задания.")
        return list(INTERVALS)


def print_result(intervals: list[float], result: ModelResult) -> None:
    """Вывести результаты расчёта в читаемом виде."""
    if math.isinf(result.next_error_time):
        next_error = "не ожидается (все ошибки найдены)"
    else:
        next_error = f"{result.next_error_time:.2f}"
    rows = [
        ("Число обнаруженных ошибок n", f"{result.n}"),
        ("Общее число ошибок B", f"{result.b:.4f} (≈ {round(result.b)})"),
        ("Осталось ошибок B - n", f"{result.remaining_errors}"),
        ("Коэффициент пропорциональности K", f"{result.k:.6f}"),
        (f"Время до {result.n + 1}-й ошибки X(n+1), ч", next_error),
        ("Время до окончания тестирования t_k, ч", f"{result.time_to_end:.2f}"),
    ]
    width = max(len(label) for label, _ in rows) + 2
    print()
    print("Интервалы Xi, ч:", ", ".join(f"{x:g}" for x in intervals))
    for label, value in rows:
        print(f"{label + ':':<{width}}{value}")


def run() -> None:
    """Точка входа приложения."""
    intervals = read_intervals()
    try:
        result = calculate(intervals)
    except ValueError as error:
        print(f"Ошибка: {error}")
        raise SystemExit(1) from error
    print_result(intervals, result)
