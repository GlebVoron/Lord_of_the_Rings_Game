from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sqlite3


class LogWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Логи игроков")
        self.setGeometry(100, 100, 800, 600)

        # Создаем таблицу для отображения логов
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Начало", "Конец", "Длительность", "Игрок", "Уровень"])

        # Настройка таблицы
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # Растягиваем столбцы
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Запрещаем редактирование

        self.load_logs()

        self.setCentralWidget(self.table)

    def load_logs(self):
        # Подключаемся к базе данных
        conn = sqlite3.connect('game_stats.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM game_sessions ORDER BY id DESC')
        logs = cursor.fetchall()
        conn.close()

        self.table.setRowCount(len(logs))
        for row, log in enumerate(logs):
            for col, data in enumerate(log):
                item = QTableWidgetItem(str(data))
                self.table.setItem(row, col, item)
