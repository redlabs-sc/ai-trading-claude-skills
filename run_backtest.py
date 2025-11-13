#!/usr/bin/env python3
"""
Strategy Validation Runner

Runs comprehensive backtests to validate trading strategy profitability.
Tests against multiple scenarios and provides go/no-go recommendation.
"""

import sys
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'cryptocurrency-trader-skill' / 'scripts'))

from backtester import Backtester, BacktestResult
from trading_agent_enhanced import EnhancedTradingAgent
from config import get_config
from fetch_historical_data import fetch_ohlcv_data, create_synthetic_data, load_historical_data


class StrategyValidator:
    """
    Validates trading strategy performance against historical data
    """

    def __init__(self, config_path: Optional[str] = None):
        """Initialize validator with configuration"""
        self.config = get_config(config_path)
        print("✅ Configuration loaded")
        print(f"   Strategy: {self.config.strategy.name} v{self.config.strategy.version}")
        print()

    def validate_strategy(
        self,
        symbol: str = 'BTC/USDT',
        timeframe: str = '1h',
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        use_synthetic: bool = False,
        synthetic_days: int = 90
    ) -> Dict:
        """
        Run backtest validation on strategy

        Args:
            symbol: Trading pair
            timeframe: Candle timeframe
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            use_synthetic: Use synthetic data instead of real
            synthetic_days: Days of synthetic data

        Returns:
            Dictionary with validation results and recommendation
        """

        print("=" * 70)
        print("STRATEGY VALIDATION - BACKTEST ANALYSIS")
        print("=" * 70)
        print()

        # Step 1: Load data
        print("📊 Step 1: Loading Historical Data")
        print("-" * 70)

        if use_synthetic:
            print(f"Creating synthetic {symbol} data...")
            df = create_synthetic_data(
                days=synthetic_days,
                symbol=symbol,
                timeframe=timeframe,
                trend='mixed',
                save_to_file=False
            )
        else:
            # Try to load from file first, then fetch if needed
            filename = f"{symbol.replace('/', '_')}_{timeframe}_{start_date or 'recent'}.csv"
            filepath = Path('data') / filename

            if filepath.exists():
                print(f"Loading from cache: {filepath}")
                df = load_historical_data(str(filepath))
            else:
                print(f"Fetching {symbol} data from exchange...")
                try:
                    df = fetch_ohlcv_data(
                        exchange_name='binance',
                        symbol=symbol,
                        timeframe=timeframe,
                        start_date=start_date,
                        end_date=end_date
                    )
                except Exception as e:
                    print(f"❌ Failed to fetch data: {e}")
                    print("💡 Falling back to synthetic data...")
                    df = create_synthetic_data(
                        days=synthetic_days,
                        symbol=symbol,
                        timeframe=timeframe,
                        trend='mixed',
                        save_to_file=False
                    )

        print()

        # Step 2: Initialize backtester
        print("🔧 Step 2: Initializing Backtesting Engine")
        print("-" * 70)

        # Create trading agent with configuration
        agent = EnhancedTradingAgent(
            balance=self.config.backtest.initial_capital,
            exchange_name='binance'
        )

        # Create backtester
        backtester = Backtester(
            agent=agent,
            initial_capital=self.config.backtest.initial_capital,
            trading_fee=self.config.backtest.trading_fee,
            slippage=self.config.backtest.slippage
        )

        print(f"   Initial Capital: ${self.config.backtest.initial_capital:,.2f}")
        print(f"   Commission: {self.config.backtest.trading_fee * 100:.2f}%")
        print(f"   Slippage: {self.config.backtest.slippage * 100:.2f}%")
        print()

        # Step 3: Run backtest
        print("🚀 Step 3: Running Backtest")
        print("-" * 70)
        print(f"   Testing {len(df)} candles...")
        print(f"   Period: {df['timestamp'].iloc[0]} to {df['timestamp'].iloc[-1]}")
        print(f"   Symbol: {symbol}")
        print()

        result = backtester.run(df, symbol)

        # Step 4: Analyze results
        print()
        print("=" * 70)
        print("BACKTEST RESULTS")
        print("=" * 70)
        print()

        self._print_results(result)

        # Step 5: Generate recommendation
        print()
        print("=" * 70)
        print("VALIDATION ASSESSMENT")
        print("=" * 70)
        print()

        assessment = self._assess_strategy(result)

        return {
            'result': result,
            'assessment': assessment,
            'data_period': (df['timestamp'].iloc[0], df['timestamp'].iloc[-1]),
            'data_points': len(df),
            'symbol': symbol
        }

    def _print_results(self, result: BacktestResult):
        """Print backtest results in formatted way"""

        # Overall Performance
        print("📈 Overall Performance:")
        print(f"   Final Balance:        ${result.final_balance:,.2f}")
        print(f"   Total Return:         {result.total_return:+.2f}%")
        print(f"   Max Drawdown:         {result.max_drawdown:.2f}%")
        print(f"   Sharpe Ratio:         {result.sharpe_ratio:.3f}")
        print(f"   Sortino Ratio:        {result.sortino_ratio:.3f}")
        print()

        # Trade Statistics
        print("📊 Trade Statistics:")
        print(f"   Total Trades:         {result.total_trades}")
        print(f"   Winning Trades:       {result.winning_trades}")
        print(f"   Losing Trades:        {result.losing_trades}")
        print(f"   Win Rate:             {result.win_rate:.1f}%")
        print(f"   Average Win:          {result.avg_win:.2f}%")
        print(f"   Average Loss:         {result.avg_loss:.2f}%")
        print(f"   Profit Factor:        {result.profit_factor:.2f}")
        print()

        # Risk Metrics
        print("⚠️  Risk Metrics:")
        print(f"   Value at Risk (95%):  ${result.var_95:,.2f}")
        print(f"   CVaR (95%):           ${result.cvar_95:,.2f}")
        print(f"   Max Consecutive Wins: {result.max_consecutive_wins}")
        print(f"   Max Consecutive Loss: {result.max_consecutive_losses}")
        print()

        # Exposure
        print("⏱️  Market Exposure:")
        print(f"   Time in Market:       {result.exposure_time:.1f}%")
        print()

    def _assess_strategy(self, result: BacktestResult) -> Dict:
        """
        Assess strategy performance against criteria

        Returns:
            Dictionary with pass/fail for each criterion and overall recommendation
        """

        criteria = {
            'profitable': {
                'value': result.total_return,
                'threshold': 0,
                'comparison': 'greater',
                'passed': result.total_return > 0,
                'description': 'Strategy is profitable'
            },
            'sharpe_ratio': {
                'value': result.sharpe_ratio,
                'threshold': 1.0,
                'comparison': 'greater',
                'passed': result.sharpe_ratio > 1.0,
                'description': 'Sharpe ratio > 1.0 (good risk-adjusted returns)'
            },
            'win_rate': {
                'value': result.win_rate,
                'threshold': 45.0,
                'comparison': 'greater',
                'passed': result.win_rate > 45.0,
                'description': 'Win rate > 45%'
            },
            'profit_factor': {
                'value': result.profit_factor,
                'threshold': 1.2,
                'comparison': 'greater',
                'passed': result.profit_factor > 1.2,
                'description': 'Profit factor > 1.2 (wins > 1.2x losses)'
            },
            'max_drawdown': {
                'value': result.max_drawdown,
                'threshold': 30.0,
                'comparison': 'less',
                'passed': result.max_drawdown < 30.0,
                'description': 'Max drawdown < 30%'
            },
            'sufficient_trades': {
                'value': result.total_trades,
                'threshold': 10,
                'comparison': 'greater',
                'passed': result.total_trades >= 10,
                'description': 'At least 10 trades for statistical significance'
            }
        }

        # Calculate pass rate
        passed_count = sum(1 for c in criteria.values() if c['passed'])
        total_count = len(criteria)
        pass_rate = (passed_count / total_count) * 100

        # Determine recommendation
        critical_passed = (
            criteria['profitable']['passed'] and
            criteria['sharpe_ratio']['passed'] and
            criteria['sufficient_trades']['passed']
        )

        if pass_rate >= 80 and critical_passed:
            recommendation = 'GO'
            confidence = 'HIGH'
            message = "✅ Strategy validation PASSED. Ready for live trading with caution."
        elif pass_rate >= 60 and criteria['profitable']['passed']:
            recommendation = 'CAUTIOUS GO'
            confidence = 'MEDIUM'
            message = "⚠️  Strategy shows promise but needs monitoring. Start with small position sizes."
        else:
            recommendation = 'NO GO'
            confidence = 'HIGH'
            message = "❌ Strategy validation FAILED. Do NOT use for live trading."

        # Print assessment
        print(f"Criteria Assessment ({passed_count}/{total_count} passed):")
        print()

        for name, criterion in criteria.items():
            status = "✅ PASS" if criterion['passed'] else "❌ FAIL"
            print(f"   {status} - {criterion['description']}")
            print(f"          Value: {criterion['value']:.2f}, Threshold: {criterion['threshold']}")

        print()
        print(f"Pass Rate: {pass_rate:.0f}%")
        print()
        print(f"RECOMMENDATION: {recommendation} (Confidence: {confidence})")
        print(f"{message}")
        print()

        return {
            'criteria': criteria,
            'passed_count': passed_count,
            'total_count': total_count,
            'pass_rate': pass_rate,
            'recommendation': recommendation,
            'confidence': confidence,
            'message': message
        }

    def run_multi_scenario_validation(self) -> Dict:
        """
        Run validation across multiple scenarios

        Tests:
        1. Bull market (synthetic up trend)
        2. Bear market (synthetic down trend)
        3. Sideways market (synthetic sideways)
        4. Mixed/realistic market (synthetic mixed)
        5. Real historical data (if available)
        """

        print("=" * 70)
        print("MULTI-SCENARIO VALIDATION")
        print("=" * 70)
        print()
        print("Testing strategy across 4 market scenarios...")
        print()

        scenarios = []

        # Scenario 1: Bull Market
        print("📊 Scenario 1: Bull Market")
        print("-" * 70)
        df_bull = create_synthetic_data(days=90, trend='up', save_to_file=False)
        agent_bull = EnhancedTradingAgent(balance=10000, exchange_name='binance')
        backtester_bull = Backtester(agent=agent_bull, initial_capital=10000)
        result_bull = backtester_bull.run(df_bull, 'BTC/USDT')
        print(f"✅ Bull Market: {result_bull.total_return:+.2f}% return, Sharpe: {result_bull.sharpe_ratio:.2f}")
        print()
        scenarios.append(('Bull Market', result_bull))

        # Scenario 2: Bear Market
        print("📊 Scenario 2: Bear Market")
        print("-" * 70)
        df_bear = create_synthetic_data(days=90, trend='down', save_to_file=False)
        agent_bear = EnhancedTradingAgent(balance=10000, exchange_name='binance')
        backtester_bear = Backtester(agent=agent_bear, initial_capital=10000)
        result_bear = backtester_bear.run(df_bear, 'BTC/USDT')
        print(f"✅ Bear Market: {result_bear.total_return:+.2f}% return, Sharpe: {result_bear.sharpe_ratio:.2f}")
        print()
        scenarios.append(('Bear Market', result_bear))

        # Scenario 3: Sideways Market
        print("📊 Scenario 3: Sideways Market")
        print("-" * 70)
        df_sideways = create_synthetic_data(days=90, trend='sideways', save_to_file=False)
        agent_sideways = EnhancedTradingAgent(balance=10000, exchange_name='binance')
        backtester_sideways = Backtester(agent=agent_sideways, initial_capital=10000)
        result_sideways = backtester_sideways.run(df_sideways, 'BTC/USDT')
        print(f"✅ Sideways Market: {result_sideways.total_return:+.2f}% return, Sharpe: {result_sideways.sharpe_ratio:.2f}")
        print()
        scenarios.append(('Sideways Market', result_sideways))

        # Scenario 4: Mixed/Realistic Market
        print("📊 Scenario 4: Mixed/Realistic Market")
        print("-" * 70)
        df_mixed = create_synthetic_data(days=90, trend='mixed', save_to_file=False)
        agent_mixed = EnhancedTradingAgent(balance=10000, exchange_name='binance')
        backtester_mixed = Backtester(agent=agent_mixed, initial_capital=10000)
        result_mixed = backtester_mixed.run(df_mixed, 'BTC/USDT')
        print(f"✅ Mixed Market: {result_mixed.total_return:+.2f}% return, Sharpe: {result_mixed.sharpe_ratio:.2f}")
        print()
        scenarios.append(('Mixed Market', result_mixed))

        # Summary
        print()
        print("=" * 70)
        print("MULTI-SCENARIO SUMMARY")
        print("=" * 70)
        print()

        print("Performance Across Scenarios:")
        print()
        print(f"{'Scenario':<20} {'Return':<12} {'Sharpe':<10} {'Win Rate':<12} {'Trades':<10}")
        print("-" * 70)

        total_return = 0
        avg_sharpe = 0
        avg_win_rate = 0
        total_trades = 0

        for name, result in scenarios:
            print(f"{name:<20} {result.total_return:>+10.2f}%  {result.sharpe_ratio:>8.2f}  {result.win_rate:>10.1f}%  {result.total_trades:>8}")
            total_return += result.total_return
            avg_sharpe += result.sharpe_ratio
            avg_win_rate += result.win_rate
            total_trades += result.total_trades

        print("-" * 70)
        avg_return = total_return / len(scenarios)
        avg_sharpe = avg_sharpe / len(scenarios)
        avg_win_rate = avg_win_rate / len(scenarios)
        print(f"{'AVERAGE':<20} {avg_return:>+10.2f}%  {avg_sharpe:>8.2f}  {avg_win_rate:>10.1f}%  {total_trades:>8}")
        print()

        # Overall assessment
        print("Overall Multi-Scenario Assessment:")
        print()

        robust = all(r.total_return > -10 for _, r in scenarios)  # No catastrophic losses
        profitable = avg_return > 0
        good_sharpe = avg_sharpe > 0.8

        if robust and profitable and good_sharpe:
            print("✅ ROBUST: Strategy performs consistently across market conditions")
        elif profitable:
            print("⚠️  CONDITIONALLY ROBUST: Strategy is profitable but shows variability")
        else:
            print("❌ NOT ROBUST: Strategy shows inconsistent performance")

        print()

        return {
            'scenarios': scenarios,
            'avg_return': avg_return,
            'avg_sharpe': avg_sharpe,
            'avg_win_rate': avg_win_rate,
            'total_trades': total_trades,
            'robust': robust,
            'profitable': profitable
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Validate trading strategy with backtesting')
    parser.add_argument('--symbol', default='BTC/USDT', help='Trading pair')
    parser.add_argument('--timeframe', default='1h', help='Timeframe')
    parser.add_argument('--start', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end', help='End date (YYYY-MM-DD)')
    parser.add_argument('--synthetic', action='store_true', help='Use synthetic data')
    parser.add_argument('--days', type=int, default=90, help='Days of synthetic data')
    parser.add_argument('--multi', action='store_true', help='Run multi-scenario validation')
    parser.add_argument('--config', help='Path to config file')

    args = parser.parse_args()

    try:
        validator = StrategyValidator(config_path=args.config)

        if args.multi:
            # Run multi-scenario validation
            results = validator.run_multi_scenario_validation()
        else:
            # Run single validation
            results = validator.validate_strategy(
                symbol=args.symbol,
                timeframe=args.timeframe,
                start_date=args.start,
                end_date=args.end,
                use_synthetic=args.synthetic,
                synthetic_days=args.days
            )

        print()
        print("=" * 70)
        print("VALIDATION COMPLETE")
        print("=" * 70)
        print()

        if args.multi:
            if results['robust'] and results['profitable']:
                print("✅ Strategy validated across multiple market conditions")
                print(f"   Average Return: {results['avg_return']:+.2f}%")
                print(f"   Average Sharpe: {results['avg_sharpe']:.2f}")
                sys.exit(0)
            else:
                print("⚠️  Strategy needs improvement for robust performance")
                sys.exit(1)
        else:
            rec = results['assessment']['recommendation']
            if rec == 'GO':
                sys.exit(0)
            elif rec == 'CAUTIOUS GO':
                sys.exit(0)
            else:
                sys.exit(1)

    except Exception as e:
        print(f"❌ Validation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
