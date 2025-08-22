import sqlite3

class DatabaseManager:
    def __init__(self, db_file="scores.db"):
        """Инициализация менеджера базы данных"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Создание таблицы результатов, если она не существует"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                name TEXT, 
                score INTEGER
            )
        ''')
        self.conn.commit()

    def save_score(self, name, score):
        """Сохранение результата игрока в базу данных"""
        self.cursor.execute(
            "INSERT INTO scores VALUES (?, ?)", 
            (name, score)
        )
        self.conn.commit()

    def get_top_scores(self, limit=5):
        """Получение топ-N результатов из базы данных"""
        self.cursor.execute(
            "SELECT name, score FROM scores ORDER BY score DESC LIMIT ?", 
            (limit,)
        )
        return self.cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()