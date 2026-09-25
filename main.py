"""Общая точка входа: запуск выбранной лабораторной работы.

    python main.py        — выбрать ЛР из меню
    python main.py 2      — сразу запустить ЛР №2
"""

import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Номер ЛР -> (папка, тема). Каждая ЛР добавляет сюда строку в своей ветке.
LABS: dict[str, tuple[str, str]] = {
    "2": ("lr2", "Модель Джелинского-Моранды"),
}


def choose_lab() -> str:
    """Спросить номер ЛР в меню."""
    print("Лабораторные работы:")
    for number, (_, title) in LABS.items():
        print(f"  {number} — {title}")
    try:
        return input("Номер ЛР: ").strip()
    except EOFError:
        print("\nВвод недоступен — укажите номер ЛР аргументом: python main.py <номер>")
        raise SystemExit(1) from None


def run_lab(number: str) -> None:
    """Запустить main.py из папки выбранной ЛР."""
    number = number.removeprefix("lr")
    if number not in LABS:
        print(f"Нет ЛР «{number}». Доступны: {', '.join(LABS)}")
        raise SystemExit(1)
    lab_dir = ROOT / LABS[number][0]
    # Пакеты ЛР импортируются от её папки, как при запуске lrN/main.py напрямую
    sys.path.insert(0, str(lab_dir))
    runpy.run_path(str(lab_dir / "main.py"), run_name="__main__")


def main() -> None:
    number = sys.argv[1] if len(sys.argv) > 1 else choose_lab()
    run_lab(number)


if __name__ == "__main__":
    main()
