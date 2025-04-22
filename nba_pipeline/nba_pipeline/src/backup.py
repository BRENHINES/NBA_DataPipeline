import os
import polars as pl
import psycopg2

def backup_table_to_parquet(conn_str: str, table_name: str, output_dir: str = "data/backups"):
    os.makedirs(output_dir, exist_ok=True)
    conn = psycopg2.connect(conn_str)
    df = pl.read_database(f"SELECT * FROM {table_name}", conn)
    path = f"{output_dir}/{table_name}.parquet"
    df.write_parquet(path)
    print(f"✅ Backup {table_name} ➡️ {path}")
    conn.close()