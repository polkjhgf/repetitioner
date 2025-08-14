import sqlite3
from typing import List, Dict

DB_PATH = "repetition.db"

def connection_db(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(conn: sqlite3.Connection):
    with conn:
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS repetition (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_day INTEGER,
            repetition_day INTEGER,
            words TEXT
        );
        """)

def insert_db(conn: sqlite3.Connection, study_day: int, repetition_day: int, words: str) -> int:
    """Добавляет запись повторения и возвращает её ID"""
    with conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO repetition (study_day, repetition_day, words)
            VALUES (?, ?, ?)
        """, (study_day, repetition_day, words))
        return c.lastrowid


def get_db(conn: sqlite3.Connection, study_day:int) -> List[Dict]:
    with conn:
        c = conn.execute("""SELECT * FROM repetition WHERE study_day = ?""", (study_day,))
        return [dict(row) for row in c.fetchall()]

def remove_db(conn: sqlite3.Connection, study_day:int, repetition_day:int) -> int:
    """Удаляет запись с заданным study_day и repetition_day"""
    with conn:
        c = conn.cursor()
        c.execute("""
            DELETE FROM repetition
            WHERE study_day = ? and repetition_day = ?
        """, (study_day, repetition_day))
        delete = c.rowcount
    return delete




