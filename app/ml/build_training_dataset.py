import sqlite3
import pandas as pd

DB_PATH = "app.db"

def extract_training_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query("""
        SELECT 
            device_id,
            physics_estimated_count,
            physics_mass_change_fg,
            ml_estimated_time_to_detection,
            ml_confidence,
            virus_id
        FROM detections
        WHERE virus_id IS NOT NULL
    """, conn)

    conn.close()
    return df

if __name__ == "__main__":
    df = extract_training_data()
    print("Extracted rows:", len(df))
    print(df.head())

    df.to_csv("app/ml/training_data.csv", index=False)
    print("Saved training_data.csv")
