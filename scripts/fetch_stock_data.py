import os
from datetime import datetime

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

# Local fallback for testing
# In GitHub Actions, DATABASE_URL secret will automatically override this
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    #"postgresql://neondb_owner:npg_GVAuC4DUhLQ6@ep-soft-cake-addafwxu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
)

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

data = []

for stock in stocks:
    try:
        ticker = yf.Ticker(stock)

        hist = ticker.history(
            period="1d",
            interval="5m"
        )

        if hist.empty:
            print(f"No data found for {stock}")
            continue

        latest = hist.iloc[-1]

        data.append({
            "timestamp": datetime.now(),
            "symbol": stock,
            "current_price": float(latest["Close"]),
            "open_price": float(latest["Open"]),
            "high_price": float(latest["High"]),
            "low_price": float(latest["Low"]),
            "volume": int(latest["Volume"])
        })

        print(f"Fetched data for {stock}")

    except Exception as e:
        print(f"Error fetching {stock}: {e}")

if not data:
    raise Exception("No stock data fetched")

df = pd.DataFrame(data)

# Create database connection
engine = create_engine(DATABASE_URL)

# Insert data into PostgreSQL
df.to_sql(
    "stock_prices",
    con=engine,
    if_exists="append",
    index=False
)

print(f"Inserted {len(df)} records successfully")