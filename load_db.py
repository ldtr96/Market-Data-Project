import pandas as pd
import logging
import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_to_pg(df):
    logging.info("Connecting to database...")
    con = psycopg2.connect(
        dbname="marketdata",
        user="marketuser",
        password="marketpass",
        host="host.docker.internal",
        port=5432
    )

    try:
        # Work on a copy and normalize DataFrame column names to lowercase
        df = df.copy()
        df.columns = df.columns.str.lower()

        logging.info("Loading existing keys from database...")
        # read existing keys; request lowercase names from DB
        existing_data = pd.read_sql("SELECT ticker, date FROM ticker_price_data", con, parse_dates=["date"])
        existing_data.columns = existing_data.columns.str.lower()

        # Normalize dates to datetime64[ns]
        if "date" not in df.columns:
            raise ValueError("Input DataFrame must contain a 'date' column")

        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        existing_data["date"] = pd.to_datetime(existing_data["date"], errors="coerce")

        # If you only care about the date part (no time), normalize to midnight
        df["date"] = df["date"].dt.normalize()
        existing_data["date"] = existing_data["date"].dt.normalize()

        # Drop rows with invalid/missing dates
        df = df[df["date"].notna()]

        logging.info("Filtering duplicate rows...")
        df_new = df.merge(existing_data, how="left", on=["ticker", "date"], indicator=True)
        df_new = df_new[df_new["_merge"] == "left_only"].drop(columns=["_merge"])

        if df_new.empty:
            logging.info("No new rows to insert.")
            # still report total rows
            with con.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM ticker_price_data")
                total_rows = cur.fetchone()[0]
                logging.info(f"Total rows in database: {total_rows}.")
            return

        # Prepare insert
        cols = list(df_new.columns)
        df_new = df_new[cols]  # deterministic order
        values = [tuple(x) for x in df_new.itertuples(index=False, name=None)]
        col_names = ", ".join(f'"{c}"' for c in cols)  # quote column names in case of reserved words
        insert_sql = f'INSERT INTO ticker_price_data ({col_names}) VALUES %s ON CONFLICT (ticker, date) DO NOTHING'

        # Bulk insert in batches inside a transaction
        with con:
            with con.cursor() as cur:
                batch_size = 10000
                for i in range(0, len(values), batch_size):
                    execute_values(cur, insert_sql, values[i:i+batch_size], page_size=1000)

            # count inside the same connection/transaction context
            with con.cursor() as cur:
                cur.execute("SELECT COUNT(*) FROM ticker_price_data")
                total_rows = cur.fetchone()[0]
                logging.info(f"Total rows in database after load: {total_rows}.")

    except Exception:
        logging.exception("Error during load_to_pg; transaction rolled back.")
        raise
    finally:
        con.close()
        logging.info("Database connection closed.")
