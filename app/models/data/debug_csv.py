import pandas as pd

CSV_PATH = "app/models/data/virus_multiclass.csv"

print("Loading CSV...")
df = pd.read_csv(CSV_PATH, encoding="utf-8", engine="python")

print("\n=== HEAD ===")
print(df.head())

print("\n=== SHAPE ===")
print(df.shape)

print("\n=== COLUMNS ===")
print(df.columns)

print("\n=== NaN COUNT PER COLUMN ===")
print(df.isna().sum())

print("\n=== Unique virus_name count ===")
print(df["virus_name"].nunique())

print("\n=== Rows with NaN virus_name ===")
print(df[df["virus_name"].isna()])
