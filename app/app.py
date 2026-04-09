import os
import psycopg2 # Змінили бібліотеку на Postgres
from flask import Flask

app = Flask(__name__)

# Функція підключення до PostgreSQL
def get_db_connection():
    # Беремо налаштування із змінних оточення, які ми вказали в docker-compose.yml
    conn = psycopg2.connect(
        host='db', # Назва сервісу в мережі Docker
        database=os.environ.get('DB_NAME', 'counter_db'),
        user=os.environ.get('DB_USER', 'user'),
        password=os.environ.get('DB_PASS', 'password')
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    # Створюємо таблицю hits
    cur.execute('CREATE TABLE IF NOT EXISTS hits (count INTEGER);')
    # Перевіряємо, чи є запис
    cur.execute('SELECT count FROM hits LIMIT 1;')
    if cur.fetchone() is None:
        cur.execute('INSERT INTO hits (count) VALUES (0);')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/')
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    # Оновлюємо лічильник
    cur.execute('UPDATE hits SET count = count + 1;')
    conn.commit()
    
    # Беремо нове значення
    cur.execute('SELECT count FROM hits LIMIT 1;')
    count = cur.fetchone()[0]
    
    cur.close()
    conn.close()
    
    return f'<h1>Hello DevOps!</h1><p>This page has been visited {count} times.</p>'

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
