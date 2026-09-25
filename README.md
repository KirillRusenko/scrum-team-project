# Проектирование информационных систем — лабораторные работы

| Папка | Тема |
|-------|------|
| `lr2/` | Модель Джелинского-Моранды |
| `lr3/` | Метрики Холстеда |
| `lr4/` | Статический анализ кода (Java) |
| `lr5/` | Оценка качества ПО по ГОСТ 28195-89 |

В каждой папке `docs/` — текст задания. Реализация каждой ЛР ведётся в отдельной ветке.

Общее для всех ЛР: `main.py`, `Dockerfile`, `ruff.toml` (линтер), `.github/workflows/ci.yml` (CI/CD),
`requirements-dev.txt` (инструменты разработки).

Запуск любой ЛР — через общую точку входа `main.py` в корне:

```bash
python3 main.py        # выбрать ЛР из меню
python3 main.py 2      # сразу запустить ЛР №2
docker build -t scrum-labs . && docker run --rm -it scrum-labs 2

pip install -r requirements-dev.txt
ruff check .
pytest lr2
```
