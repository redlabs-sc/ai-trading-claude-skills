#!/usr/bin/env python3
"""
Historical Data Fetcher for Backtesting

Fetches OHLCV data from cryptocurrency exchanges for backtesting.
Supports multiple exchanges and saving data locally for reuse.
"""

import sys
import ccxt
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import json
import time
from typing import Optional, List

def fetch_ohlcv_data(
    exchange_name: str = 'binance',
    symbol: str = 'BTC/USDT',
    timeframe: str = '1h',
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: int = 1000,
    save_to_file: bool = True
) -> pd.DataFrame:
    """
    Fetch historical OHLCV data from exchange

    Args:
        exchange_name: Exchange to use (binance, kraken, coinbase, etc.)
        symbol: Trading pair (e.g., 'BTC/USDT')
        timeframe: Candle timeframe ('1m', '5m', '15m', '1h', '4h', '1d')
        start_date: Start date (YYYY-MM-DD format)
        end_date: End date (YYYY-MM-DD format)
        limit: Max candles per request (500-1000 typical)
        save_to_file: Save data to CSV file

    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
    """

    print(f"Fetching {symbol} {timeframe} data from {exchange_name}...")

    # Initialize exchange
    exchange_class = getattr(ccxt, exchange_name)
    exchange = exchange_class({
        'enableRateLimit': True,
        'timeout': 30000
    })

    # Parse dates
    if start_date:
        since = exchange.parse8601(f"{start_date}T00:00:00Z")
    else:
        # Default to 3 months ago
        since = exchange.parse8601((datetime.now() - timedelta(days=90)).strftime("%Y-%m-%dT00:00:00Z"))

    if end_date:
        until = exchange.parse8601(f"{end_date}T23:59:59Z")
    else:
        until = exchange.milliseconds()

    # Fetch data in chunks
    all_ohlcv = []
    current_since = since

    print(f"  Period: {datetime.fromtimestamp(since/1000)} to {datetime.fromtimestamp(until/1000)}")
    print(f"  Fetching in chunks of {limit} candles...")

    chunk_count = 0
    while current_since < until:
        try:
            # Fetch OHLCV
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=current_since, limit=limit)

            if not ohlcv:
                break

            all_ohlcv.extend(ohlcv)
            chunk_count += 1

            # Update since to last candle timestamp + 1
            current_since = ohlcv[-1][0] + 1

            print(f"  Chunk {chunk_count}: Fetched {len(ohlcv)} candles (total: {len(all_ohlcv)})")

            # Rate limiting
            time.sleep(exchange.rateLimit / 1000)

        except Exception as e:
            print(f"  Error fetching data: {e}")
            break

    if not all_ohlcv:
        raise ValueError("No data fetched from exchange")

    # Convert to DataFrame
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

    # Remove duplicates
    df = df.drop_duplicates(subset=['timestamp']).reset_index(drop=True)

    print(f"\n✅ Fetched {len(df)} candles")
    print(f"   Period: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
    print(f"   Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")

    # Save to file
    if save_to_file:
        filename = f"{symbol.replace('/', '_')}_{timeframe}_{start_date or 'recent'}.csv"
        filepath = Path('data') / filename
        filepath.parent.mkdir(exist_ok=True)

        df.to_csv(filepath, index=False)
        print(f"   Saved to: {filepath}")

    return df


def load_historical_data(filepath: str) -> pd.DataFrame:
    """Load historical data from CSV file"""
    df = pd.read_csv(filepath)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df


def create_synthetic_data(
    days: int = 90,
    starting_price: float = 40000,
    symbol: str = 'BTC/USDT',
    timeframe: str = '1h',
    trend: str = 'mixed',
    save_to_file: bool = True
) -> pd.DataFrame:
    """
    Create synthetic OHLCV data for testing when exchange not available

    Args:
        days: Number of days of data
        starting_price: Starting price
        symbol: Symbol name (for filename)
        timeframe: Timeframe (for filename)
        trend: 'up', 'down', 'sideways', or 'mixed'
        save_to_file: Save to CSV

    Returns:
        DataFrame with realistic OHLCV data
    """
    import numpy as np

    print(f"Creating synthetic {symbol} {timeframe} data...")
    print(f"  Days: {days}")
    print(f"  Starting price: ${starting_price:,.2f}")
    print(f"  Trend: {trend}")

    np.random.seed(42)  # Reproducible

    # Create timestamps
    if timeframe == '1h':
        periods = days * 24
        freq = 'H'
    elif timeframe == '4h':
        periods = days * 6
        freq = '4H'
    elif timeframe == '15m':
        periods = days * 96
        freq = '15min'
    else:
        periods = days * 24
        freq = 'H'

    timestamps = pd.date_range(
        start=datetime.now() - timedelta(days=days),
        periods=periods,
        freq=freq
    )

    # Generate price data with realistic characteristics
    prices = [starting_price]

    for i in range(1, periods):
        # Base drift based on trend
        if trend == 'up':
            drift = 0.0002  # 0.02% per candle upward
        elif trend == 'down':
            drift = -0.0002
        elif trend == 'sideways':
            drift = 0
        else:  # mixed
            # Alternate between up and down trends
            cycle_length = 100
            drift = 0.0003 * np.sin(i / cycle_length * 2 * np.pi)

        # Add volatility
        volatility = 0.015  # 1.5% typical volatility
        change = drift + np.random.randn() * volatility

        # Apply change
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, starting_price * 0.5))  # Don't go below 50% of start

    prices = np.array(prices)

    # Create OHLC from close prices
    df = pd.DataFrame({
        'timestamp': timestamps,
        'close': prices
    })

    # Generate realistic OHLC
    df['open'] = df['close'].shift(1).fillna(df['close'])
    df['high'] = df[['open', 'close']].max(axis=1) * (1 + np.abs(np.random.randn(len(df)) * 0.003))
    df['low'] = df[['open', 'close']].min(axis=1) * (1 - np.abs(np.random.randn(len(df)) * 0.003))
    df['volume'] = np.random.lognormal(mean=10, sigma=0.5, size=len(df))

    # Reorder columns
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]

    print(f"\n✅ Created {len(df)} candles")
    print(f"   Period: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
    print(f"   Price range: ${df['close'].min():.2f} - ${df['close'].max():.2f}")
    print(f"   Final price: ${df['close'].iloc[-1]:.2f}")
    print(f"   Return: {((df['close'].iloc[-1] / df['close'].iloc[0]) - 1) * 100:+.2f}%")

    # Save to file
    if save_to_file:
        filename = f"{symbol.replace('/', '_')}_{timeframe}_synthetic_{days}d.csv"
        filepath = Path('data') / filename
        filepath.parent.mkdir(exist_ok=True)

        df.to_csv(filepath, index=False)
        print(f"   Saved to: {filepath}")

    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch historical data for backtesting')
    parser.add_argument('--exchange', default='binance', help='Exchange name')
    parser.add_argument('--symbol', default='BTC/USDT', help='Trading pair')
    parser.add_argument('--timeframe', default='1h', help='Timeframe (1h, 4h, etc.)')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--synthetic', action='store_true', help='Create synthetic data instead')
    parser.add_argument('--days', type=int, default=90, help='Days of data (for synthetic)')

    args = parser.parse_args()

    if args.synthetic:
        # Create synthetic data
        df = create_synthetic_data(
            days=args.days,
            symbol=args.symbol,
            timeframe=args.timeframe,
            trend='mixed'
        )
    else:
        # Fetch real data from exchange
        try:
            df = fetch_ohlcv_data(
                exchange_name=args.exchange,
                symbol=args.symbol,
                timeframe=args.timeframe,
                start_date=args.start,
                end_date=args.end
            )
        except Exception as e:
            print(f"\n❌ Error fetching data: {e}")
            print("\nTip: If you don't have exchange access, use --synthetic flag:")
            print(f"  python {sys.argv[0]} --synthetic --days 90")
            sys.exit(1)

    print("\n✅ Data ready for backtesting!")
    print(f"   Shape: {df.shape}")
    print(f"   Columns: {list(df.columns)}")
