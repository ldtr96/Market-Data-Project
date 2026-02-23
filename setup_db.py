import sqlite3

#Sets up the table to be used in the SQLite DB market_data_db
con = sqlite3.connect("market_data.db")
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS ticker_price_data(
            Ticker TEXT NOT NULL,
            Date TEXT NOT NULL,
            Open REAL,
            Close REAL,
            Intraday_Difference REAL,
            percent_chg_price REAL,
            High REAL,
            Low REAL,
            Volume REAL,
            Volume_Price_Trend REAL,
            PRIMARY KEY (Ticker, Date)
            )
""")

con.commit