import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_lib.db')
cursor = connection.cursor()

# Обновляем таблицу books, добавляя новое поле comments
cursor.execute('''
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    author TEXT NOT NULL,
    genre TEXT NOT NULL,
    rating TEXT NOT NULL,
    status TEXT NOT NULL,
    pdf_path TEXT,
    comments TEXT
)
''')

# Проверяем, есть ли уже колонка comments, если нет - добавляем
cursor.execute("PRAGMA table_info(books)")
columns = [column[1] for column in cursor.fetchall()]
if 'comments' not in columns:
    cursor.execute("ALTER TABLE books ADD COLUMN comments TEXT")

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
