import pandas as pd

from .config import StrategyConfig
from .indicators import calculate_atr, calculate_ema, calculate_macd, calculate_rsi


def generate_signals(df: pd.DataFrame, config: StrategyConfig | None = None) -> pd.DataFrame:
    if config is None:
        config = StrategyConfig()

    data = df.copy()
    data["ema_fast"] = calculate_ema(data["Close"], config.fast_ema)
    data["ema_slow"] = calculate_ema(data["Close"], config.slow_ema)
    data["rsi"] = calculate_rsi(data["Close"], config.rsi_window)
    macd = calculate_macd(data["Close"], fast_span=12, slow_span=26, signal_span=9)
    data["macd"] = macd["macd"]
    data["macd_signal"] = macd["signal"]
    data["atr"] = calculate_atr(data, config.atr_window)

    data["signal"] = 0

    buy_mask = (
        (data["ema_fast"] > data["ema_slow"]) &
        (data["rsi"] > 50) &
        (data["macd"] > data["macd_signal"])
    )

    sell_mask = (
        (data["ema_fast"] < data["ema_slow"]) |
        (data["rsi"] < 50) |
        (data["macd"] < data["macd_signal"])
    )

    data.loc[buy_mask, "signal"] = 1
    data.loc[sell_mask, "signal"] = -1

    data["stop_loss"] = data["Close"] - (data["atr"] * config.stop_loss_atr)
    data["take_profit"] = data["Close"] + (data["atr"] * config.stop_loss_atr)

    return data
