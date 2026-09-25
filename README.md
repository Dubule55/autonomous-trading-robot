# Autonomous Trading Robot Starter

This project is a beginner-friendly, fully working trading robot starter that uses a simple technical strategy to decide when to buy and sell.

Features:
- Python-based trading bot starter
- Buy/sell signal generation using EMA + RSI logic
- Backtesting engine with position tracking and P&L
- Market data loader (Yahoo Finance or synthetic fallback)
- CLI to run a simulation

## Project structure

- `trading_bot/` – core bot logic
- `requirements.txt` – Python dependencies
- `README.md` – project overview and instructions

## Quick start

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   # .venv\Scripts\activate    # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run a backtest:
   ```bash
   python -m trading_bot.main --symbol AAPL --initial-cash 10000 --days 180
   ```

4. Or run with a custom date range:
   ```bash
   python -m trading_bot.main --symbol MSFT --initial-cash 5000 --start-date 2023-01-01 --end-date 2024-01-01
   ```

## Trading logic

The starter strategy uses:
- EMA fast vs slow crossover
- RSI trend confirmation
- Basic risk control through stop-loss and position sizing

This is a learning and testing template, not a guaranteed money-making system.

## Important note

This project is for educational and research purposes. Real trading involves risk, commissions, slippage, and market volatility.
