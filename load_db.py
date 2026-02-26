import sqlite3
import pandas as pd

#Loads dataframe from the MarketData-Modular file into SQLite DB market_data.db
def load_to_sqlite(df):
    con = sqlite3.connect("market_data.db")
    
    existing_data = pd.read_sql('SELECT Ticker, Date FROM ticker_price_data',con)

    df_new = df.merge(existing_data,how="left",on=["Ticker","Date"],indicator=True)
    df_new = df_new[df_new["_merge"]=="left_only"].drop(columns=["_merge"])
    df_new.to_sql("ticker_price_data",con, if_exists="append", index = False)

    # Verify how many rows are in the DB now.
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM ticker_price_data")
    print("Total rows in table:", cur.fetchone()[0])

    con.close()
    