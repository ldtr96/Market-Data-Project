import yfinance as yf
import pandas as pd
import sqlite3
from IngestTransform import get_price_history, calculate_metrics
from load_db import load_to_sqlite
import argparse
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),               # prints to console
        logging.FileHandler("pipeline.log")    # writes to file
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
@app.get("/data/{ticker}")
async def get_prices(ticker:str, start_date: str = None, end_date: str= None):
    query = "SELECT * FROM ticker_price_data WHERE Ticker = ?"
    params=[ticker]
    if start_date:
        query +=" AND Date >= ?"
        params.append(start_date)
    
    if end_date:
        query +=" AND Date <= ?"
        params.append(end_date)
    
    conn = sqlite3.connect("market_data.db")
    logging.info("Connection to market_data.db opened...")
    df = pd.read_sql(query,conn,params=tuple(params))
    conn.close()
    logging.info("Connection to market_data.db closed.")
    if df.empty:
        raise HTTPException(status_code=404, detail=f"No data found for {ticker}.")
    return {"Ticker":ticker, "data":df.to_dict(orient="records")}

#Orchestration
def orchestrate_data(ticker):
    logging.info("Getting price history...")
    t_info = get_price_history(ticker)
    logging.info("Calculating metrics...")
    t_info = calculate_metrics(t_info,ticker)
    logging.info("Loading to SQLite Database...")
    load_to_sqlite(t_info)
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
    