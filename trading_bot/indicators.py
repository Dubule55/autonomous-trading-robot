import numpy as np
import pandas as pd


def calculate_ema(series: pd.Series, span: int) -> pd.Series:
    return series.ewm(span=span, adjust=False).mean()


def calculate_rsi(series: pd.Series, window: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def calculate_macd(series: pd.Series, fast_span: int = 12, slow_span: int = 26, signal_span: int = 9):
    fast = calculate_ema(series, fast_span)
    slow = calculate_ema(series, slow_span)
    macd = fast - slow
    signal = macd.ewm(span=signal_span, adjust=False).mean()
    histogram = macd - signal
    return {
        "macd": macd,
        "signal": signal,
        "histogram": histogram,
    }


def calculate_atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    tr = pd.concat(
        [
            (high - low),
            (high - close.shift(1)).abs(),
            (low - close.shift(1)).abs(),
        ],
        axis=1,
    ).max(axis=1)

    return tr.rolling(window=window, min_periods=window).mean()
