# Market-Data-Project
Repository for financial data pipeline project.

The initial purpose of this project is to ingest financial data (historical stock price data) using the yfinance library. The yfinance library is an open source tool that allows users to fetch financial data from Yahoo Finance. Once the data is ingested, I transform the data and calculate additional metrics using the Pandas library. The data is then loaded into a SQLite database named market_data.db. This is to be run every Saturday to fetch the last 5 trading days worth of information for any given stock given the ticker symbol e.g. AAPL.

The setup for the SQLite database is to be run once by prefixing the CREATE TABLE function with IF NOT EXISTS. There shouldn't be any issue in subsequent runs. A primary key was also created on the combination of ticker and date, so data cannot be duplicated. 

I will add logging and error handling soon.


