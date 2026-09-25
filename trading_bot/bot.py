from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf


def generate_synthetic_data(symbol: str, start_date: str, end_date: str, days: int = 365):
    np.random.seed(42)
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    if len(dates) == 0:
        dates = pd.date_range(start=(datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d"), end=datetime.now().strftime("%Y-%m-%d"), freq="D")

    price = 100.0
    closes = []
    opens = []
    highs = []
    lows = []

    for i in range(len(dates)):
        drift = 0.02 * np.sin(i / 12)
        shock = np.random.normal(0, 1.5) / 100
        price = max(10, price * (1 + drift + shock))
        close = round(price, 2)

        opens.append(round(close * (1 + np.random.uniform(-0.02, 0.02)), 2))
        highs.append(round(max(open := opens[-1], close) * (1 + np.random.uniform(0.01, 0.04)), 2))
        lows.append(round(min(open, close) * (1 - np.random.uniform(0.01, 0.04)), 2))
        closes.append(close)

    df = pd.DataFrame({
        "Open": opens,
        "High": highs,
        "Low": lows,
        "Close": closes,
        "Volume": np.random.randint(1000, 500000, size=len(dates)),
    }, index=dates)
    df.columns = [col for col in df.columns]
    return df


def load_market_data(symbol: str, start_date: str | None = None, end_date: str | None = None, days: int = 180, interval: str = "1d"):
    end = end_date or datetime.now().strftime("%Y-%m-%d")
    if start_date is None:
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    else:
        start = start_date

    try:
        data = yf.download(symbol, start=start, end=end, interval=interval, progress=False, auto_adjust=True)
        if data.empty:
            raise ValueError("No data returned from Yahoo Finance")
        data = data.reset_index().rename(columns={"Date": "Date"})
        data = data.rename(columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume",
        })
        data = data.set_index("Date")
        return data
    except Exception:
        return generate_synthetic_data(symbol, start, end, days)
