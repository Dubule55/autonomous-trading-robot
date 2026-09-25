import argparse
from datetime import datetime, timedelta

from .bot import TradingBot


def parse_args():
    parser = argparse.ArgumentParser(description="Autonomous trading bot starter")
    parser.add_argument("--symbol", type=str, default="AAPL", help="Ticker symbol to simulate")
    parser.add_argument("--initial-cash", type=float, default=10000.0, help="Starting cash amount")
    parser.add_argument("--start-date", type=str, default=None, help="Optional start date in YYYY-MM-DD format")
    parser.add_argument("--end-date", type=str, default=None, help="Optional end date in YYYY-MM-DD format")
    parser.add_argument("--days", type=int, default=180, help="Number of past days to load when no date range is provided")
    return parser.parse_args()


def main():
    args = parse_args()
    bot = TradingBot()
    result = bot.run(
        symbol=args.symbol,
        initial_cash=args.initial_cash,
        start_date=args.start_date,
        end_date=args.end_date,
        days=args.days,
    )

    print(f"Symbol: {args.symbol}")
    print(f"Initial cash: ${result['initial_cash']:.2f}")
    print(f"Final equity: ${result['final_equity']:.2f}")
    print(f"Return: {result['total_return'] * 100:.2f}%")
    print(f"Total trades: {result['total_trades']}")
    print(f"Profitable trades: {result['profit_trades']}")
    print(f"Gross profit: ${result['gross_profit']:.2f}")


if __name__ == "__main__":
    main()
