import sqlite3
import pandas as pd
import logging
import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_to_pg (df):
    logging.info("Connecting to database...")
    con = psycopg2.connect(
        dbname="marketdata",
        user="marketuser",
        password="marketpass",
        host="host.docker.internal",
        port=5432
    )

    logging.info("loading existing keys from database...")
    # normalize Date columns before merging
    existing_data = pd.read_sql('SELECT Ticker, Date FROM ticker_price_data', con, parse_dates=['Date'])
    df = df.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
    df = df[df['Date'].notna()]
    existing_data['Date'] = pd.to_datetime(existing_data['Date'], errors='coerce')

    # optional: if you only care about the date (no time component)
    df['Date'] = df['Date'].dt.normalize()
    existing_data['Date'] = existing_data['Date'].dt.normalize()

    # drop rows with invalid/missing dates to avoid merge surprises
    df = df[df['Date'].notna()]

    logging.info("Filtering duplicate rows...")
    df_new = df.merge(existing_data, how="left", on=["Ticker", "Date"], indicator=True)
    df_new = df_new[df_new["_merge"] == "left_only"].drop(columns=["_merge"])

    if not df_new.empty:
        cols = list(df_new.columns)
        df_new = df_new[cols]  # ensure deterministic column order
    values = [tuple(x) for x in df_new.itertuples(index=False, name=None)]
    col_names = ", ".join(f'"{c}"' for c in cols)
    insert_sql = f'INSERT INTO ticker_price_data ({col_names}) VALUES %s ON CONFLICT (Ticker, Date) DO NOTHING'
    with con:
        with con.cursor() as cur:
            batch_size = 10000
            for i in range(0, len(values), batch_size):
                execute_values(cur, insert_sql, values[i:i+batch_size], page_size=1000)

    #Verify how many rows are in the DB now.

    cur.execute("SELECT COUNT(*) FROM ticker_price_data")
    total_rows = cur.fetchone()[0]
    logging.info(f"Total rows in database after load: {total_rows}.")

    con.close()
    logging.info("Database connection closed.")

    