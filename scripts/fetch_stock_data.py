import os
from datetime import datetime

import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set.")

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

        hist = yf.download(
            stock,
            period="5d",
            interval="5m",
            progress=False,
            auto_adjust=False,
            threads=False
        )

        print(f"\n===== {stock} =====")
        print(hist.tail())

        if hist.empty:
            print(f"No data found for {stock}")
            continue

        # Flatten MultiIndex columns if present
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)

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

        print(f"Fetched {stock}")

    except Exception as e:
        print(f"Error fetching {stock}: {e}")

if not data:
    print("No stock data fetched.")
    exit(0)

df = pd.DataFrame(data)

print(df)

engine = create_engine(DATABASE_URL)

df.to_sql(
    "stock_prices",
    con=engine,
    if_exists="append",
    index=False
)

print(f"Inserted {len(df)} records successfully.")