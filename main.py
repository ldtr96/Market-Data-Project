import yfinance as yf
import pandas as pd
import sqlite3
from IngestTransform import get_price_history, calculate_metrics
from load_db import load_to_sqlite

#This shall be the main file where the orchestration and run should occur.

#Orchestration

def orchestrate_data(ticker):
    t_info = get_price_history(ticker)
    t_info = calculate_metrics(t_info,ticker)
    t_info = load_to_sqlite(t_info)
    return t_info

#Main logic will go here