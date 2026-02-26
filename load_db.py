import sqlite3
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),               # prints to console
        logging.FileHandler("pipeline.log")    # writes to file
    ]
)


#Loads dataframe from the MarketData-Modular file into SQLite DB market_data.db
def load_to_sqlite(df):
    logging.info("Connecting to database...")
    con = sqlite3.connect("market_data.db")
    
    logging.info("loading existing keys from database...")
    existing_data = pd.read_sql('SELECT Ticker, Date FROM ticker_price_data',con)

    logging.info("Filtering duplicate rows...")
    df_new = df.merge(existing_data,how="left",on=["Ticker","Date"],indicator=True)
    df_new = df_new[df_new["_merge"]=="left_only"].drop(columns=["_merge"])
    df_new.to_sql("ticker_price_data",con, if_exists="append", index = False)

    logging.info(f"{len(df_new)} new rows to insert.")

    # Verify how many rows are in the DB now.
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM ticker_price_data")
    total_rows = cur.fetchone()[0]
    logging.info(f"Total rows in database after load: {total_rows}.")

    con.close()
    logging.info("Database connection closed.")
    