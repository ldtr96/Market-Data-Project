import yfinance as yf
import pandas as pd
import sqlite3
from IngestTransform import get_price_history, calculate_metrics
from load_db import load_to_sqlite
import argparse
import logging

#This shall be the main file where the orchestration and run should occur.

#Orchestration

def orchestrate_data(ticker):
    logging.info("Getting price history...")
    t_info = get_price_history(ticker)
    logging.info("Calculating metrics...")
    t_info = calculate_metrics(t_info,ticker)
    logging.info("Loading to SQLite Database...")
    #t_info = load_to_sqlite(t_info)
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
    logging.info(f"user input ticker: {ticker}.")
    #Orchestration function using the argument passed in with the help of argparse.
    t_info = orchestrate_data(ticker)

    return t_info

if __name__ == "__main__":
    print(main())