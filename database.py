import sqlite3
import pandas as pd

DB_NAME = "workflows.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS execution_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_prompt TEXT,
            extracted_trigger TEXT,
            extracted_action TEXT,
            status TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_log(raw_prompt, trigger, action, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO execution_logs (raw_prompt, extracted_trigger, extracted_action, status)
        VALUES (?, ?, ?, ?)
    ''', (raw_prompt, trigger, action, status))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM execution_logs ORDER BY id DESC", conn)
    conn.close()
    return df

def clear_all_logs():
    """Clear all records from the execution_logs table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM execution_logs')
    conn.commit()
    conn.close()