FROM python:3.12-slim

WORKDIR /app
COPY . .

# Зависимости ставятся, только если в репозитории есть requirements.txt
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Общая точка входа; номер ЛР передаётся аргументом: docker run -it <образ> 2
ENTRYPOINT ["python", "main.py"]
