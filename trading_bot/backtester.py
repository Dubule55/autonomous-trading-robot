from __future__ import annotations

import numpy as np
import pandas as pd

from .strategy import generate_signals


class Backtester:
    def __init__(self, data: pd.DataFrame, initial_cash: float = 10000.0, commission: float = 0.001):
        self.data = data.copy()
        self.initial_cash = initial_cash
        self.commission = commission
        self.cash = initial_cash
        self.position = 0
        self.entry_price = 0.0
        self.trades = []
        self.equity_curve = []

    def run(self):
        for index, row in self.data.iterrows():
            close_price = float(row["Close"])
            signal = int(row["signal"])
            equity = self.cash + (self.position * close_price)
            self.equity_curve.append({"date": index, "equity": equity})

            if signal == 1 and self.position <= 0:
                shares_to_buy = int(self.cash / (close_price * (1 + self.commission)))
                if shares_to_buy > 0:
                    self.cash -= shares_to_buy * close_price * (1 + self.commission)
                    self.position = shares_to_buy
                    self.entry_price = close_price
                    self.trades.append({
                        "type": "buy",
                        "date": index,
                        "price": close_price,
                        "shares": shares_to_buy,
                    })

            elif signal == -1 and self.position > 0:
                proceeds = self.position * close_price * (1 - self.commission)
                pnl = proceeds - (self.position * self.entry_price)
                self.cash += proceeds
                self.trades.append({
                    "type": "sell",
                    "date": index,
                    "price": close_price,
                    "shares": self.position,
                    "pnl": pnl,
                })
                self.position = 0
                self.entry_price = 0.0

            if self.position > 0 and float(row["Close"]) <= float(row["stop_loss"]):
                proceeds = self.position * close_price * (1 - self.commission)
                pnl = proceeds - (self.position * self.entry_price)
                self.cash += proceeds
                self.trades.append({
                    "type": "stop_loss",
                    "date": index,
                    "price": close_price,
                    "shares": self.position,
                    "pnl": pnl,
                })
                self.position = 0
                self.entry_price = 0.0

        final_equity = self.cash + (self.position * self.data["Close"].iloc[-1])
        total_return = (final_equity - self.initial_cash) / self.initial_cash

        profitable_trades = 0
        for trade in self.trades:
            if trade.get("pnl") is not None and trade["pnl"] > 0:
                profitable_trades += 1

        gross_profit = sum(trade.get("pnl", 0) for trade in self.trades if trade.get("pnl") is not None)

        return {
            "initial_cash": self.initial_cash,
            "final_cash": self.cash,
            "final_equity": final_equity,
            "total_return": total_return,
            "profit_trades": profitable_trades,
            "total_trades": len(self.trades),
            "gross_profit": gross_profit,
            "equity_curve": self.equity_curve,
            "trades": self.trades,
        }
