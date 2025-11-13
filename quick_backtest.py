#!/usr/bin/env python3
"""
Quick Backtest Runner

Simple script to run a single backtest and see results.
Avoids network connections by using synthetic data.
"""

import sys
from pathlib import Path
import pandas as pd

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'cryptocurrency-trader-skill' / 'scripts'))

from backtester import Backtester, BacktestResult
from fetch_historical_data import create_synthetic_data


def create_mock_agent(balance: float = 10000):
    """
    Create a mock trading agent that doesn't require network connection
    """
    class MockAgent:
        def __init__(self, balance):
            self.balance = balance
            self.exchange_name = 'binance'

        def comprehensive_analysis(self, symbol, df):
            """
            Simple mock analysis based on RSI
            Returns buy/sell/hold signals compatible with backtester
            """
            # Calculate simple RSI
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0).rolling(window=14).mean()
            loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
            rs = gain / loss.replace(0, 1e-10)
            rsi = 100 - (100 / (1 + rs))

            # Simple strategy: Buy when RSI < 35, Sell when RSI > 65
            last_rsi = rsi.iloc[-1] if not rsi.empty else 50

            if pd.isna(last_rsi):
                return {'signal': 'hold', 'confidence': 50}

            if last_rsi < 35:
                return {
                    'signal': 'buy',
                    'confidence': 70,
                    'stop_loss': df['close'].iloc[-1] * 0.98,  # 2% stop loss
                    'take_profit': df['close'].iloc[-1] * 1.04  # 4% take profit
                }
            elif last_rsi > 65:
                return {
                    'signal': 'sell',
                    'confidence': 70,
                    'stop_loss': df['close'].iloc[-1] * 1.02,  # 2% stop loss
                    'take_profit': df['close'].iloc[-1] * 0.96  # 4% take profit
                }
            else:
                return {'signal': 'hold', 'confidence': 50}

    return MockAgent(balance)


def run_quick_backtest(days: int = 90, trend: str = 'mixed'):
    """Run a quick backtest with synthetic data"""

    print("=" * 70)
    print("QUICK BACKTEST - STRATEGY VALIDATION")
    print("=" * 70)
    print()

    # Step 1: Create synthetic data
    print("📊 Creating synthetic data...")
    df = create_synthetic_data(
        days=days,
        trend=trend,
        save_to_file=False
    )
    print()

    # Step 2: Create mock agent
    print("🔧 Initializing mock trading agent...")
    agent = create_mock_agent(balance=10000)
    print("   Initial Capital: $10,000.00")
    print("   Strategy: Simple RSI (< 35 = buy, > 65 = sell)")
    print()

    # Step 3: Run backtest
    print("🚀 Running backtest...")
    backtester = Backtester(
        agent=agent,
        initial_capital=10000,
        trading_fee=0.001,  # 0.1%
        slippage=0.0005     # 0.05%
    )

    result = backtester.run(df, 'BTC/USDT')
    print()

    # Step 4: Display results
    print("=" * 70)
    print("BACKTEST RESULTS")
    print("=" * 70)
    print()

    print("📈 Overall Performance:")
    print(f"   Initial Balance:      ${10000:,.2f}")
    print(f"   Final Balance:        ${result.final_balance:,.2f}")
    print(f"   Total Return:         {result.total_return:+.2f}%")
    print(f"   Max Drawdown:         {result.max_drawdown:.2f}%")
    print(f"   Sharpe Ratio:         {result.sharpe_ratio:.3f}")
    print(f"   Sortino Ratio:        {result.sortino_ratio:.3f}")
    print()

    print("📊 Trade Statistics:")
    print(f"   Total Trades:         {result.total_trades}")
    print(f"   Winning Trades:       {result.winning_trades}")
    print(f"   Losing Trades:        {result.losing_trades}")
    print(f"   Win Rate:             {result.win_rate:.1f}%")
    print(f"   Average Win:          {result.avg_win:.2f}%")
    print(f"   Average Loss:         {result.avg_loss:.2f}%")
    print(f"   Profit Factor:        {result.profit_factor:.2f}")
    print()

    print("⚠️  Risk Metrics:")
    print(f"   Value at Risk (95%):  ${result.var_95:,.2f}")
    print(f"   CVaR (95%):           ${result.cvar_95:,.2f}")
    print(f"   Time in Market:       {result.exposure_time:.1f}%")
    print()

    # Assessment
    print("=" * 70)
    print("ASSESSMENT")
    print("=" * 70)
    print()

    criteria_passed = 0
    criteria_total = 6

    print("Criteria:")
    print()

    # 1. Profitable
    if result.total_return > 0:
        print("   ✅ Strategy is profitable")
        criteria_passed += 1
    else:
        print("   ❌ Strategy is not profitable")

    # 2. Sharpe ratio
    if result.sharpe_ratio > 1.0:
        print("   ✅ Good risk-adjusted returns (Sharpe > 1.0)")
        criteria_passed += 1
    else:
        print("   ❌ Poor risk-adjusted returns (Sharpe <= 1.0)")

    # 3. Win rate
    if result.win_rate > 45:
        print("   ✅ Acceptable win rate (> 45%)")
        criteria_passed += 1
    else:
        print("   ❌ Low win rate (<= 45%)")

    # 4. Profit factor
    if result.profit_factor > 1.2:
        print("   ✅ Good profit factor (> 1.2)")
        criteria_passed += 1
    else:
        print("   ❌ Low profit factor (<= 1.2)")

    # 5. Max drawdown
    if result.max_drawdown < 30:
        print("   ✅ Acceptable drawdown (< 30%)")
        criteria_passed += 1
    else:
        print("   ❌ High drawdown (>= 30%)")

    # 6. Sufficient trades
    if result.total_trades >= 10:
        print("   ✅ Sufficient trades for analysis (>= 10)")
        criteria_passed += 1
    else:
        print("   ❌ Insufficient trades (< 10)")

    print()
    print(f"Pass Rate: {(criteria_passed / criteria_total) * 100:.0f}% ({criteria_passed}/{criteria_total})")
    print()

    if criteria_passed >= 5:
        print("✅ BACKTEST PASSED - Strategy shows promise")
        print()
        return 0
    elif criteria_passed >= 3:
        print("⚠️  MIXED RESULTS - Strategy needs improvement")
        print()
        return 0
    else:
        print("❌ BACKTEST FAILED - Strategy not recommended")
        print()
        return 1


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Run quick backtest')
    parser.add_argument('--days', type=int, default=90, help='Days of data')
    parser.add_argument('--trend', default='mixed', choices=['up', 'down', 'sideways', 'mixed'], help='Market trend')

    args = parser.parse_args()

    sys.exit(run_quick_backtest(days=args.days, trend=args.trend))
