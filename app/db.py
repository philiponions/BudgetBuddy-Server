import sqlite3


def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.execute(' PRAGMA foreign_keys=ON; ')
    conn.row_factory = sqlite3.Row
    return conn
