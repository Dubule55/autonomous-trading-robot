from __future__ import annotations

from .backtester import Backtester
from .config import StrategyConfig
from .data_loader import load_market_data
from .strategy import generate_signals


class TradingBot:
    def __init__(self, config: StrategyConfig | None = None):
        self.config = config or StrategyConfig()

    def run(self, symbol: str, initial_cash: float = 10000.0, start_date: str | None = None, end_date: str | None = None, days: int = 180):
        market_data = load_market_data(symbol, start_date=start_date, end_date=end_date, days=days)
        signal_data = generate_signals(market_data, self.config)
        backtester = Backtester(signal_data, initial_cash=initial_cash)
        return backtester.run()
