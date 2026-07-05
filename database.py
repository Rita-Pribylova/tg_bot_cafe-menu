import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "cafe.db")


def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price INTEGER NOT NULL,
                category TEXT NOT NULL
            )
        """)
        cursor.execute("SELECT COUNT(*) FROM menu")
        if cursor.fetchone()[0] == 0:
            items = [
                ("Капучино", 210, "Кофе"),
                ("Латте", 210, "Кофе"),
                ("Американо", 190, "Кофе"),
                ("Эспрессо", 190, "Кофе"),
                ("Круассан классический", 150, "Выпечка"),
                ("Чизкейк Нью-Йорк", 240, "Выпечка"),
                ("Пицца Маргарита", 300, "Выпечка"),
                ("Сырная пицца", 300, "Выпечка"),
            ]
            cursor.executemany(
                "INSERT INTO menu (name, price, category) VALUES (?, ?, ?)",
                items,
            )
            conn.commit()
            print("=== ТЕСТОВЫЕ ТОВАРЫ УСПЕШНО ЗАПИСАНЫ В БАЗУ ===")


def get_categories():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu")
        return [row[0] for row in cursor.fetchall()]


def get_items_by_category(category: str):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, price FROM menu WHERE category = ?", (category,)
        )
        return cursor.fetchall()


def get_item_by_id(item_id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, price FROM menu WHERE id = ?", (item_id,))
        return cursor.fetchone()
