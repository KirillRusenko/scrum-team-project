FROM python:3.12-slim

WORKDIR /app
COPY . .

# Зависимости ставятся, только если в репозитории есть requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Укажите точку входа вашей программы
CMD ["python", "main.py"]
