import math

import pytest

from jelinski_moranda.cli import parse_intervals
from jelinski_moranda.data import INTERVALS
from jelinski_moranda.model import (
    calculate,
    coefficient_k,
    next_error_time,
    time_to_end,
)
from jelinski_moranda.solver import b_equation, estimate_b, find_root


def test_find_root_simple():
    assert find_root(lambda x: x * x - 2, 0, 2, eps=1e-10) == pytest.approx(math.sqrt(2))


def test_find_root_same_sign():
    with pytest.raises(ValueError):
        find_root(lambda x: x * x + 1, -1, 1)


def test_estimate_b_is_root():
    b = estimate_b(INTERVALS)
    assert b > len(INTERVALS)
    assert b_equation(INTERVALS)(b) == pytest.approx(0, abs=1e-9)


def test_k_matches_definition():
    # K = n / sum((B - i + 1) * Xi) — первая форма формулы из задания
    b = estimate_b(INTERVALS)
    expected = len(INTERVALS) / sum(
        (b - i + 1) * x for i, x in enumerate(INTERVALS, start=1)
    )
    assert coefficient_k(INTERVALS, b) == pytest.approx(expected)


def test_variant_1():
    result = calculate(INTERVALS)
    assert result.n == 26
    assert result.b == pytest.approx(31.2159, abs=1e-4)
    assert result.k == pytest.approx(0.0068494, abs=1e-7)
    assert result.remaining_errors == 5
    assert result.next_error_time == pytest.approx(27.99, abs=0.01)
    assert result.time_to_end == pytest.approx(333.36, abs=0.01)


def test_next_error_and_time_to_end():
    assert next_error_time(n=10, b=12, k=0.5) == pytest.approx(1)
    # осталось 2 ошибки: (1/K) * (1 + 1/2)
    assert time_to_end(n=10, b=12, k=0.5) == pytest.approx(3)
    assert time_to_end(n=10, b=10.2, k=0.5) == 0


def test_all_errors_found():
    # корень уравнения меньше n — все ошибки уже обнаружены
    result = calculate([1, 2, 3, 4, 10, 20])
    assert result.b < result.n
    assert result.remaining_errors == 0
    assert math.isinf(result.next_error_time)
    assert result.time_to_end == 0


def test_not_growing_intervals():
    # интервалы уменьшаются — надёжность не растёт, конечной оценки B нет
    with pytest.raises(ValueError):
        estimate_b([10, 8, 6, 4, 2])


def test_invalid_input():
    with pytest.raises(ValueError):
        estimate_b([5])
    with pytest.raises(ValueError):
        estimate_b([1, 0, 3])


def test_parse_intervals():
    assert parse_intervals("9 12,11; 4.5") == [9, 12, 11, 4.5]
