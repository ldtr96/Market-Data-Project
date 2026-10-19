import yfinance as yf
import pandas as pd
from IngestTransform import get_price_history, calculate_metrics
from load_db import load_to_pg
import argparse
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "pipeline.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),               # prints to console
        logging.FileHandler(LOG_FILE)    # writes to file
    ]
)
#initialize instance of the FastAPI class.
app = FastAPI()

#Configuring CORS to allow passing to React
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:5173",   # ← add this, this is your React app
    "http://127.0.0.1:5173",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Setting up an endpoint to query the SQLite DB
# Postgres-backed endpoint
@app.get("/data/{ticker}")
def get_prices(ticker: str, start_date: str = None, end_date: str = None):
    # build SQL and params
    query = "SELECT * FROM ticker_price_data WHERE ticker = %s"
    params = [ticker]

    # validate/normalize date inputs to YYYY-MM-DD (or YYYY-MM-DD HH:MM:SS)
    def _normalize_date_param(d):
        if d is None:
            return None
        ts = pd.to_datetime(d, errors="coerce")
        if pd.isna(ts):
            raise HTTPException(status_code=400, detail=f"Invalid date: {d}")
        return ts.strftime("%Y-%m-%d %H:%M:%S")

    if start_date:
        params.append(_normalize_date_param(start_date))
        query += " AND date >= %s"

    if end_date:
        params.append(_normalize_date_param(end_date))
        query += " AND date <= %s"

    conn = None
    try:
        conn = psycopg2.connect(
            dbname="marketdata",
            user="marketuser",
            password="marketpass",
            host="host.docker.internal",
            port=5432
        )
        logging.info("Connection to Postgres opened for API request...")
        df = pd.read_sql(query, conn, params=tuple(params), parse_dates=["date"])
    except HTTPException:
        # re-raise validation errors
        raise
    except Exception:
        logging.exception("Database error while servicing API request")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        if conn is not None:
            conn.close()
            logging.info("Connection to Postgres closed for API request.")

    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}.")

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.strftime("%Y-%m-%d %H:%M:%S")

    return {"ticker": ticker, "data": df.to_dict(orient="records")}


#Orchestration
def orchestrate_data(ticker):
    logging.info("Getting price history...")
    t_info = get_price_history(ticker)
    logging.info("Calculating metrics...")
    t_info = calculate_metrics(t_info,ticker)
    logging.info("Loading to Postgres Database...")
    # ensure column names match Postgres (lowercase) and date is normalized
    t_info = t_info.copy()
    t_info.columns = t_info.columns.str.lower()
    # parse/normalize date column to midnight timestamps (loader expects datetime-like)
    if "date" in t_info.columns:
        t_info["date"] = pd.to_datetime(t_info["date"], errors="coerce").dt.normalize()
        t_info = t_info[t_info["date"].notna()]

    load_to_pg(t_info)
    return t_info

#Main logic will go here

def main():
    #Creates a required argument to be passed in via command line.
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ticker",
        help="The ticker of the position you want to import.",
        required=True
        )
    args = parser.parse_args()
    ticker = args.ticker
    logging.info(f"Starting run for ticker: {ticker}.")
    #Orchestration function using the argument passed in with the help of argparse.
    t_info = orchestrate_data(ticker)
    logging.info(f"Finished run for ticker: {ticker}.")

    return t_info

if __name__ == "__main__":
    print(main())
    