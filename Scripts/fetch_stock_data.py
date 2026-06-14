import yfinance as yf
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://neondb_owner:npg_GVAuC4DUhLQ6@ep-soft-cake-addafwxu-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

stocks = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

data = []

for stock in stocks:
    ticker = yf.Ticker(stock)
    info = ticker.info

    data.append({
        "timestamp": datetime.now(),
        "symbol": stock,
        "current_price": info.get("currentPrice"),
        "open_price": info.get("open"),
        "high_price": info.get("dayHigh"),
        "low_price": info.get("dayLow"),
        "volume": info.get("volume")
    })

df = pd.DataFrame(data)

engine = create_engine(DATABASE_URL)

df.to_sql(
    "stock_prices",
    engine,
    if_exists="append",
    index=False
)

print("Data Loaded Successfully")