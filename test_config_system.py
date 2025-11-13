#!/usr/bin/env python3
"""
Test configuration management system
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'cryptocurrency-trader-skill' / 'scripts'))

from config import Config, get_config

def test_config_loading():
    """Test that configuration loads successfully"""
    print("=" * 70)
    print("Test 1: Configuration Loading")
    print("=" * 70)

    try:
        config = get_config()
        print(f"  ✅ Configuration loaded: {config}")
        return True
    except Exception as e:
        print(f"  ❌ Failed to load configuration: {e}")
        return False

def test_indicator_config():
    """Test indicator configuration values"""
    print("\n" + "=" * 70)
    print("Test 2: Indicator Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  RSI Period: {config.indicators.rsi_period}")
    print(f"  RSI Overbought: {config.indicators.rsi_overbought}")
    print(f"  RSI Oversold: {config.indicators.rsi_oversold}")
    print(f"  MACD Fast: {config.indicators.macd_fast}")
    print(f"  MACD Slow: {config.indicators.macd_slow}")
    print(f"  MACD Signal: {config.indicators.macd_signal}")
    print(f"  Bollinger Period: {config.indicators.bb_period}")
    print(f"  Bollinger Std: {config.indicators.bb_std}")

    # Validate values
    assert config.indicators.rsi_period == 14, "RSI period should be 14"
    assert config.indicators.macd_fast == 12, "MACD fast should be 12"
    assert config.indicators.macd_slow == 26, "MACD slow should be 26"

    print("  ✅ All indicator configs correct")
    return True

def test_risk_management_config():
    """Test risk management configuration"""
    print("\n" + "=" * 70)
    print("Test 3: Risk Management Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  Max Risk per Trade: {config.risk.max_risk_per_trade * 100}%")
    print(f"  Max Position Size: {config.risk.max_position_size * 100}%")
    print(f"  Min Risk/Reward: {config.risk.min_risk_reward}")
    print(f"  Stop Loss ATR Mult: {config.risk.stop_loss_atr_mult}")
    print(f"  Take Profit ATR Mult: {config.risk.take_profit_atr_mult}")

    # Validate values
    assert config.risk.max_risk_per_trade == 0.02, "Max risk should be 2%"
    assert config.risk.max_position_size == 0.10, "Max position should be 10%"
    assert config.risk.min_risk_reward == 1.5, "Min R:R should be 1.5"

    print("  ✅ All risk management configs correct")
    return True

def test_bayesian_config():
    """Test Bayesian configuration"""
    print("\n" + "=" * 70)
    print("Test 4: Bayesian Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  RSI Accuracy: {config.bayesian.rsi_accuracy * 100}%")
    print(f"  MACD Accuracy: {config.bayesian.macd_accuracy * 100}%")
    print(f"  Bollinger Accuracy: {config.bayesian.bollinger_accuracy * 100}%")
    print(f"  Volume Accuracy: {config.bayesian.volume_accuracy * 100}%")
    print(f"  Trend Accuracy: {config.bayesian.trend_accuracy * 100}%")
    print(f"  Pattern Accuracy: {config.bayesian.pattern_accuracy * 100}%")
    print(f"  Initial Prior: {config.bayesian.initial_prior}")

    # Validate values
    assert config.bayesian.rsi_accuracy == 0.65, "RSI accuracy should be 65%"
    assert config.bayesian.macd_accuracy == 0.68, "MACD accuracy should be 68%"
    assert config.bayesian.initial_prior == 0.50, "Initial prior should be 0.50"

    print("  ✅ All Bayesian configs correct")
    return True

def test_monte_carlo_config():
    """Test Monte Carlo configuration"""
    print("\n" + "=" * 70)
    print("Test 5: Monte Carlo Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  Number of Simulations: {config.monte_carlo.num_simulations:,}")
    print(f"  Days Ahead: {config.monte_carlo.days_ahead}")
    print(f"  Max Exponent: {config.monte_carlo.max_exponent}")
    print(f"  Min Data Points: {config.monte_carlo.min_data_points}")

    # Validate values
    assert config.monte_carlo.num_simulations == 10000, "Should have 10,000 simulations"
    assert config.monte_carlo.days_ahead == 5, "Should forecast 5 days ahead"
    assert config.monte_carlo.max_exponent == 5.0, "Max exponent should be 5.0"

    print("  ✅ All Monte Carlo configs correct")
    return True

def test_validation_config():
    """Test validation configuration"""
    print("\n" + "=" * 70)
    print("Test 6: Validation Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  Strict Mode: {config.validation.strict_mode}")
    print(f"  Min Data Points: {config.validation.min_data_points}")
    print(f"  Max Z-Score: {config.validation.max_z_score}")
    print(f"  Benford P-Value: {config.validation.benford_p_value}")
    print(f"  Max Age (minutes): {config.validation.max_age_minutes}")
    print(f"  Min Confidence: {config.validation.min_confidence}%")
    print(f"  Max Confidence: {config.validation.max_confidence}%")

    # Validate values
    assert config.validation.strict_mode == True, "Strict mode should be enabled"
    assert config.validation.min_data_points == 20, "Min data points should be 20"
    assert config.validation.max_z_score == 5.0, "Max Z-score should be 5.0"

    print("  ✅ All validation configs correct")
    return True

def test_market_categories():
    """Test market categories"""
    print("\n" + "=" * 70)
    print("Test 7: Market Categories")
    print("=" * 70)

    config = get_config()

    for category, symbols in config.market_categories.items():
        print(f"  {category}: {len(symbols)} symbols")

    all_symbols = config.get_all_symbols()
    print(f"\n  Total symbols: {len(all_symbols)}")
    print(f"  Sample: {', '.join(all_symbols[:5])}")

    # Validate
    assert len(config.market_categories) > 0, "Should have market categories"
    assert len(all_symbols) > 0, "Should have symbols"
    assert 'BTC/USDT' in all_symbols, "Should include BTC/USDT"

    print("  ✅ Market categories loaded correctly")
    return True

def test_config_validation():
    """Test configuration validation"""
    print("\n" + "=" * 70)
    print("Test 8: Configuration Validation")
    print("=" * 70)

    config = get_config()

    is_valid = config.validate()

    if is_valid:
        print("  ✅ Configuration passed all validation checks")
    else:
        print("  ❌ Configuration failed validation")

    return is_valid

def test_backtesting_config():
    """Test backtesting configuration"""
    print("\n" + "=" * 70)
    print("Test 9: Backtesting Configuration")
    print("=" * 70)

    config = get_config()

    print(f"  Initial Capital: ${config.backtest.initial_capital:,.2f}")
    print(f"  Trading Fee: {config.backtest.trading_fee * 100}%")
    print(f"  Slippage: {config.backtest.slippage * 100}%")
    print(f"\n  Performance Targets:")
    print(f"    Min Sharpe Ratio: {config.backtest.min_sharpe_ratio}")
    print(f"    Min Win Rate: {config.backtest.min_win_rate * 100}%")
    print(f"    Min Profit Factor: {config.backtest.min_profit_factor}")
    print(f"    Max Drawdown: {config.backtest.max_drawdown * 100}%")

    # Validate values
    assert config.backtest.initial_capital == 10000, "Initial capital should be $10,000"
    assert config.backtest.min_sharpe_ratio == 1.0, "Min Sharpe should be 1.0"
    assert config.backtest.min_win_rate == 0.50, "Min win rate should be 50%"

    print("  ✅ All backtesting configs correct")
    return True

def test_usage_example():
    """Show usage example"""
    print("\n" + "=" * 70)
    print("Test 10: Usage Example")
    print("=" * 70)

    print("\n  Example: Using config in code")
    print("  " + "-" * 66)

    config = get_config()

    # Example 1: RSI calculation
    print(f"""
  # Calculate RSI with configured period
  rsi_period = config.indicators.rsi_period  # {config.indicators.rsi_period}
  rsi = calculate_rsi(prices, period=rsi_period)

  # Check overbought/oversold
  if rsi > config.indicators.rsi_overbought:  # {config.indicators.rsi_overbought}
      signal = 'OVERBOUGHT'
  elif rsi < config.indicators.rsi_oversold:  # {config.indicators.rsi_oversold}
      signal = 'OVERSOLD'
    """)

    # Example 2: Risk management
    print(f"""
  # Calculate position size with configured risk
  max_risk = account_balance * config.risk.max_risk_per_trade  # {config.risk.max_risk_per_trade * 100}%
  position_size = max_risk / (entry_price - stop_loss)

  # Check position size limit
  max_position = account_balance * config.risk.max_position_size  # {config.risk.max_position_size * 100}%
  position_size = min(position_size, max_position / entry_price)
    """)

    print("  ✅ Usage examples shown")
    return True

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("CONFIGURATION SYSTEM TEST SUITE")
    print("=" * 70)
    print()

    results = []

    try:
        results.append(("Configuration loading", test_config_loading()))
        results.append(("Indicator configuration", test_indicator_config()))
        results.append(("Risk management configuration", test_risk_management_config()))
        results.append(("Bayesian configuration", test_bayesian_config()))
        results.append(("Monte Carlo configuration", test_monte_carlo_config()))
        results.append(("Validation configuration", test_validation_config()))
        results.append(("Market categories", test_market_categories()))
        results.append(("Configuration validation", test_config_validation()))
        results.append(("Backtesting configuration", test_backtesting_config()))
        results.append(("Usage example", test_usage_example()))
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nConfiguration system ready:")
        print("  ✅ YAML configuration file (config.yaml)")
        print("  ✅ Type-safe configuration loader (config.py)")
        print("  ✅ 150+ parameters externalized")
        print("  ✅ Validation system")
        print("  ✅ Singleton pattern for global access")
        print("\nUsage:")
        print("  from scripts.config import get_config")
        print("  config = get_config()")
        print("  rsi_period = config.indicators.rsi_period")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed")
        sys.exit(1)
