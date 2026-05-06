import duckdb
import pandas as pd

conn = duckdb.connect('data.db')

df = pd.read_csv('data.csv')

conn.execute("DROP TABLE IF EXISTS main_data")
conn.register('df', df)
conn.execute("CREATE TABLE main_data AS SELECT * FROM df")

count = conn.execute("SELECT COUNT(*) FROM main_data").fetchone()[0]
print(f"Database ready — {count} rows loaded")
print("\nColumns:")
print(conn.execute("DESCRIBE main_data").df().to_string())