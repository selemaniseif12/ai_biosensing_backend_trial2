import sqlite3
import pandas as pd

DB_PATH = "app.db"

def list_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [t[0] for t in tables]

def show_columns(table):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table});")
    cols = cursor.fetchall()
    conn.close()
    return cols

def extract_table(table):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

if __name__ == "__main__":
    print("📌 Listing tables in app.db:")
    tables = list_tables()
    for t in tables:
        print(" -", t)

    print("\n📌 Showing columns for each table:")
    for t in tables:
        print(f"\nTable: {t}")
        cols = show_columns(t)
        for col in cols:
            print("   ", col)

    print("\nRun again after selecting the correct table for training.")
