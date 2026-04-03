FROM python:3.11-slim
WORKDIR /app

# Копіюємо requirements саме з папки app
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо ВМІСТ твоєї папки app прямо в /app контейнера
COPY app/ .

EXPOSE 5000
CMD ["python", "app.py"]