import sqlite3
import datetime
import time

start_time = 0
end_time = 0
username = ""
level_passed = ""


# Функция для создания таблицы в базе данных
def create_table():
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration TEXT,
            username TEXT NOT NULL,
            level_passed TEXT
        )
    ''')
    conn.commit()
    conn.close()


def take_end_time(time):
    global end_time
    end_time = time


def take_start_time(time):
    global start_time
    start_time = time


def take_username(name):
    global username
    username = name


def take_level_passed(stat):
    global level_passed
    level_passed = stat


# Функция для записи данных о завершении прохождения уровня
def record_level_session():
    global end_time
    global start_time
    global level_passed
    global username
    duration = end_time - start_time

    if not username:
        username = "Аноним"
    if not end_time:
        end_time = 0
    if not start_time:
        start_time = 0
    if not level_passed:
        level_passed = "Ошибка"

    # Записываем данные в базу данных
    conn = sqlite3.connect('game_stats.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO game_sessions (start_time, end_time, duration, username, level_passed)
        VALUES (?, ?, ?, ?, ?)
    ''', (start_time, end_time, str(duration), username, level_passed))
    conn.commit()
    conn.close()


# Пример использования
if __name__ == "__main__":
    create_table()

