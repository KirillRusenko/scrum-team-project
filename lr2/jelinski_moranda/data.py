"""Входные данные: интервалы между ошибками Xi (часы), вариант 1 из задания (таблица 1).

Значения хранятся в общей конфигурации проекта (.env в корне репозитория,
переменная LR2_INTERVALS). Если .env нет, берётся шаблон .env.example.
Переменная окружения процесса имеет приоритет над файлом.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env" if (ROOT / ".env").is_file() else ROOT / ".env.example"


def read_env_file(path: Path) -> dict[str, str]:
    """Прочитать пары KEY=VALUE из .env-файла (пустые строки и # комментарии пропускаются)."""
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        values[key.strip()] = value.strip().strip("\"'")
    return values


def load_intervals(path: Path = ENV_FILE) -> list[float]:
    """Получить интервалы Xi из переменной LR2_INTERVALS (числа через запятую или пробел)."""
    raw = os.environ.get("LR2_INTERVALS") or read_env_file(path).get("LR2_INTERVALS")
    if not raw:
        raise RuntimeError(f"Не задана переменная LR2_INTERVALS (файл {path})")
    try:
        return [float(p) for p in raw.replace(";", " ").replace(",", " ").split()]
    except ValueError as error:
        raise RuntimeError(f"LR2_INTERVALS должна содержать только числа: {raw!r}") from error


INTERVALS: list[float] = load_intervals()
