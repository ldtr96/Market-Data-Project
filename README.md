# Market-Data-Project
Repository for financial data pipeline project.

The purpose of this project is to ingest financial data (historical stock price data) using the yfinance library. The yfinance library is an open source tool that allows users to fetch financial data from Yahoo Finance. Once the data is ingested, I transform the data and calculate additional metrics using the Pandas library. The data is then loaded into a SQLite database named market_data.db. This is to be run every Saturday to fetch the last 5 trading days worth of information for any given stock given the ticker symbol e.g. AAPL. There is also a FastAPI REST Endpoint for /data/{ticker}. This serves data from the market_data.db to the user via the endpoint.

# File structure
```
├── main.py             # Entry point, orchestrates ETL pipeline
├── IngestTransform.py  # Fetches and transforms stock data via yfinance
├── load_db.py          # Loads transformed data into SQLite
├── setup_db.py         # One-time DB schema setup (run separately)
├── market_data.db      # SQLite database (auto-generated)
└── requirements.txt
```

# Setting Up the Project

The External libraries required in this project can be found in the requirements.txt file.

The main packages to install if requirements.txt is not used are:
- yfinance
- uvicorn
- pandas
- fastapi

# 1. Create a virtual environment for your project
Navigate to the folder your project will be housed using your CLI of choice. Mine is CMD.

If your VScode did not already create a virtual environment, navigate to your respective folder and type: python -m venv ('Enter your virtual environment name here.')

# 2. Pip install the packages from requirements.txt

In your command line, type python -m pip install -r requirements.txt

# How to run the data loader:
There are a couple of ways to run the program:
- The first is to run via the CLI. You navigate to your project folder in the virtual environment, and type python main.py --ticker ('Your Ticker of choice').
    - This actually runs the loader and ingests, transforms, and loads the database with the stock data you want.
- The second is to run using the batch_scheduler.bat file. You will want to keep the .bat file in the same directory as everything else. You will also need to edit your .bat file for the tickers you want to ingest. Currently it is set up to ingest the last 5 trading days for AAPL, MSFT, & NVDA. Feel free to add more tickers to run in the .bat file.

# How to query the REST API endpoint:
When you want to query the REST endpoint for a specific ticker:
- Make sure uvicorn is installed.
- Go to your CLI and type: python -m uvicorn main:app --reload
- Once the live server is up and running, go to your browser and type: http://127.0.0.1:8000/docs to bring up the Swagger UI.
- Test the API end point and query for your ticker with start and end date as optional parameters.


# Data Output

The following metrics are stored in market_data.db for each ticker and trading date:

| Column | Description |
|---|---|
| Ticker | Stock symbol (e.g. AAPL) |
| Date | Trading date |
| Open | Opening price |
| Close | Closing price |
| High | Intraday high price |
| Low | Intraday low price |
| Volume | Number of shares traded |
| Intraday_Difference | Difference between Close and Open (Close - Open) |
| percent_chg_price | Percentage change from Open to Close |
| Volume_Price_Trend | Volume weighted by price change direction (a momentum indicator) |

# Note 

The primary key on the sqlite database is a combination of Ticker and Date, so re-running the pipeline won't duplicate entries. Logic in the load_db.py file also prevents duplicate entries.











