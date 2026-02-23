import json
import yfinance as yf
import pandas as pd

#This is for important metrics crucial for fundamental investing and fundamental analysis.
def get_fundamentals(ticker):
    ticker_info = yf.Ticker(ticker)
    info = ticker_info.info
    ticker_extract = ['debtToEquity','returnOnEquity','currentRatio','priceEpsCurrentYear']
    return {k: info.get(k) for k in ticker_extract}

#This is for for some other data if needed. Read the yfinance API docs for more info.
def get_extra_info(ticker):
    t = yf.Ticker(ticker)
    t_calendar = t.calendar
    t_price_targets = t.analyst_price_targets
    t_quarter_income_statements = t.quarterly_income_stmt
    t_options = t.option_chain(t.options[0]).calls
    return t_calendar, t_price_targets, t_quarter_income_statements, t_options

#This is to download actual current/historical market data including date, price, open, close, high, low, and volume.
def get_price_history(ticker):
    t = yf.download(ticker,period='5d')
    return t

#Add column to calculate the intraday difference between the opening price and closing price to
#measure movement & percent change & Volume Price Trend.
def calculate_metrics(df,ticker):
    df=df.copy()
    df['Intraday_Difference']= df['Close']-df['Open']
    df['percent_chg_price']=((df['Close']-df['Open'])/df['Open'])*100
    df['Volume_Price_Trend']=round(df[('Volume',ticker)]*df['percent_chg_price'],4)
    df['Ticker'] = ticker

    # Reset index if needed
    if df.index.name == 'Date':
        df = df.reset_index()

    # Re-order the columns before loading into SQLite DB
    ordered_cols = [
        'Ticker',
        'Date',
        'Open',
        'Close',
        'Intraday_Difference',
        'percent_chg_price',
        'High',
        'Low',
        'Volume',
        'Volume_Price_Trend'
    ]
    return df[ordered_cols]

























