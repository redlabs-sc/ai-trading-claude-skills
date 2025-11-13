#!/usr/bin/env python3
"""
Quick verification test for GBM systematic bias fix
Tests that Monte Carlo simulation produces unbiased results
"""

import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'cryptocurrency-trader-skill' / 'scripts'))

from advanced_analytics import AdvancedAnalytics

def test_gbm_unbiased():
    """
    Test that GBM produces unbiased results with zero drift

    With zero mean returns, the expected price should equal current price
    (within statistical tolerance)
    """
    print("=" * 70)
    print("Testing GBM Systematic Bias Fix")
    print("=" * 70)

    analytics = AdvancedAnalytics()

    # Create synthetic returns with zero mean (no drift)
    np.random.seed(42)  # Reproducible results
    returns = pd.Series(np.random.normal(0, 0.02, 100))  # Mean=0, Std=2%

    current_price = 100.0

    print(f"\nTest Parameters:")
    print(f"  Current Price: ${current_price}")
    print(f"  Returns Mean: {returns.mean():.6f} (should be ~0)")
    print(f"  Returns Std: {returns.std():.4f}")
    print(f"  Simulations: 10,000")
    print(f"  Days Ahead: 5")

    # Run Monte Carlo simulation
    result = analytics.monte_carlo_simulation(current_price, returns, days_ahead=5, num_simulations=10000)

    if 'error' in result:
        print(f"\n❌ ERROR: {result['error']}")
        return False

    expected_price = result['expected_price']
    expected_return = result['expected_return_pct']

    print(f"\nResults:")
    print(f"  Expected Price: ${expected_price:.2f}")
    print(f"  Expected Return: {expected_return:.2f}%")
    print(f"  5th Percentile: ${result['price_5th_percentile']:.2f}")
    print(f"  Median: ${result['price_median']:.2f}")
    print(f"  95th Percentile: ${result['price_95th_percentile']:.2f}")

    # With zero drift, expected price should be very close to current price
    # Allow 2% tolerance due to sampling variance
    bias = abs(expected_price - current_price) / current_price

    print(f"\nBias Analysis:")
    print(f"  Absolute Bias: {bias*100:.2f}%")
    print(f"  Tolerance: 2.0%")

    if bias < 0.02:
        print("\n✅ PASS: GBM appears unbiased (bias < 2%)")
        print("   Itô's Lemma correction is working correctly!")
        return True
    else:
        print("\n⚠️  WARNING: GBM shows bias > 2%")
        print("   This might indicate the fix didn't work or sampling variance")
        return False

def test_gbm_positive_drift():
    """
    Test that GBM works correctly with positive drift
    """
    print("\n" + "=" * 70)
    print("Testing GBM with Positive Drift")
    print("=" * 70)

    analytics = AdvancedAnalytics()

    # Create returns with positive mean (upward drift)
    np.random.seed(43)
    returns = pd.Series(np.random.normal(0.01, 0.02, 100))  # Mean=1%, Std=2%

    current_price = 100.0

    print(f"\nTest Parameters:")
    print(f"  Current Price: ${current_price}")
    print(f"  Returns Mean: {returns.mean():.4f} (positive drift)")
    print(f"  Returns Std: {returns.std():.4f}")

    result = analytics.monte_carlo_simulation(current_price, returns, days_ahead=5, num_simulations=10000)

    if 'error' in result:
        print(f"\n❌ ERROR: {result['error']}")
        return False

    print(f"\nResults:")
    print(f"  Expected Price: ${result['expected_price']:.2f}")
    print(f"  Expected Return: {result['expected_return_pct']:.2f}%")

    # With positive drift, expected price should be higher than current
    if result['expected_price'] > current_price:
        print("\n✅ PASS: Positive drift produces higher expected price")
        return True
    else:
        print("\n❌ FAIL: Positive drift should produce higher expected price")
        return False

def test_gbm_no_crash():
    """
    Test that GBM doesn't crash with various inputs
    """
    print("\n" + "=" * 70)
    print("Testing GBM Robustness (No Crashes)")
    print("=" * 70)

    analytics = AdvancedAnalytics()

    test_cases = [
        ("Low volatility", np.random.normal(0, 0.001, 100)),
        ("High volatility", np.random.normal(0, 0.05, 100)),
        ("Negative drift", np.random.normal(-0.01, 0.02, 100)),
    ]

    all_passed = True
    for name, returns_data in test_cases:
        returns = pd.Series(returns_data)
        np.random.seed(44)
        result = analytics.monte_carlo_simulation(100.0, returns, days_ahead=5, num_simulations=1000)

        if 'error' in result:
            print(f"  ❌ {name}: {result['error']}")
            all_passed = False
        else:
            print(f"  ✅ {name}: Expected ${result['expected_price']:.2f}")

    return all_passed

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("GBM FIX VERIFICATION TEST SUITE")
    print("=" * 70)

    results = []

    # Run all tests
    results.append(("Zero drift (unbiased test)", test_gbm_unbiased()))
    results.append(("Positive drift", test_gbm_positive_drift()))
    results.append(("Robustness", test_gbm_no_crash()))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! GBM fix is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please review the results above.")
        sys.exit(1)
