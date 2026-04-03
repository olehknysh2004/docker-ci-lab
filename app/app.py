_import os
import sqlite3
from flask import Flask

app = Flask(__name__)

# Використовуємо SQLite замість PostgreSQL для простоти
def get_db_connection():
    # Створює файл database.db прямо в папці /app всередині контейнера
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    # Створюємо таблицю, якщо її немає
    conn.execute('CREATE TABLE IF NOT EXISTS hits (count INTEGER);')
    
    # Перевіряємо, чи є вже запис, якщо ні — додаємо нуль
    cur = conn.cursor()
    cur.execute('SELECT count FROM hits LIMIT 1;')
    if cur.fetchone() is None:
        conn.execute('INSERT INTO hits (count) VALUES (0);')
    
    conn.commit()
    conn.close()

@app.route('/')
def hello():
    conn = get_db_connection()
    # Оновлюємо лічильник
    conn.execute('UPDATE hits SET count = count + 1;')
    conn.commit()
    
    # Беремо нове значення
    cur = conn.cursor()
    cur.execute('SELECT count FROM hits LIMIT 1;')
    count = cur.fetchone()[0]
    conn.close()
    
    return f'<h1>Hello DevOps!</h1><p>This page has been visited {count} times.</p>'

if __name__ == "__main__":
    init_db()
    # Слухаємо на всіх інтерфейсах (0.0.0.0), щоб Docker міг "прокинути" порт
    app.run(host="0.0.0.0", port=5000)
