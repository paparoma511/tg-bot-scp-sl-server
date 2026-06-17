import sqlite3

DB_NAME = "cards.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        cards_opened INTEGER DEFAULT 0,
        last_open INTEGER DEFAULT 0
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cards(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        rarity TEXT,
        card_name TEXT
    )
    """)

    conn.commit()
    conn.close()