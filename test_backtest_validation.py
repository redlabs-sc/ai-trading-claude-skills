#!/usr/bin/env python3
"""
Tests for Backtest Validation System

Validates that the strategy validation framework works correctly.
"""

import unittest
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent / 'cryptocurrency-trader-skill' / 'scripts'))

from run_backtest import StrategyValidator
from fetch_historical_data import create_synthetic_data


class TestBacktestValidation(unittest.TestCase):
    """Test suite for backtest validation system"""

    def setUp(self):
        """Set up test fixtures"""
        self.validator = StrategyValidator()

    def test_validator_initialization(self):
        """Test that validator initializes correctly"""
        self.assertIsNotNone(self.validator)
        self.assertIsNotNone(self.validator.config)
        print("✓ Validator initialization works")

    def test_single_validation_synthetic(self):
        """Test single validation with synthetic data"""
        result = self.validator.validate_strategy(
            symbol='BTC/USDT',
            timeframe='1h',
            use_synthetic=True,
            synthetic_days=30  # Short test
        )

        # Check that we got results
        self.assertIsNotNone(result)
        self.assertIn('result', result)
        self.assertIn('assessment', result)

        # Check result structure
        backtest_result = result['result']
        self.assertIsNotNone(backtest_result.total_return)
        self.assertIsNotNone(backtest_result.sharpe_ratio)
        self.assertIsNotNone(backtest_result.total_trades)

        print(f"✓ Single validation works")
        print(f"  Return: {backtest_result.total_return:+.2f}%")
        print(f"  Sharpe: {backtest_result.sharpe_ratio:.2f}")
        print(f"  Trades: {backtest_result.total_trades}")

    def test_assessment_criteria(self):
        """Test that assessment criteria are evaluated correctly"""
        result = self.validator.validate_strategy(
            use_synthetic=True,
            synthetic_days=30
        )

        assessment = result['assessment']

        # Check assessment structure
        self.assertIn('criteria', assessment)
        self.assertIn('recommendation', assessment)
        self.assertIn('confidence', assessment)
        self.assertIn('pass_rate', assessment)

        # Check all criteria are present
        expected_criteria = [
            'profitable',
            'sharpe_ratio',
            'win_rate',
            'profit_factor',
            'max_drawdown',
            'sufficient_trades'
        ]

        for criterion in expected_criteria:
            self.assertIn(criterion, assessment['criteria'])
            self.assertIn('passed', assessment['criteria'][criterion])

        print(f"✓ Assessment criteria work")
        print(f"  Recommendation: {assessment['recommendation']}")
        print(f"  Pass Rate: {assessment['pass_rate']:.0f}%")

    def test_multi_scenario_validation(self):
        """Test multi-scenario validation"""
        results = self.validator.run_multi_scenario_validation()

        # Check results structure
        self.assertIn('scenarios', results)
        self.assertIn('avg_return', results)
        self.assertIn('avg_sharpe', results)
        self.assertIn('robust', results)

        # Check we have 4 scenarios
        self.assertEqual(len(results['scenarios']), 4)

        # Check each scenario has name and result
        for name, result in results['scenarios']:
            self.assertIsNotNone(name)
            self.assertIsNotNone(result)
            self.assertIsNotNone(result.total_return)

        print(f"✓ Multi-scenario validation works")
        print(f"  Scenarios tested: {len(results['scenarios'])}")
        print(f"  Average return: {results['avg_return']:+.2f}%")
        print(f"  Average Sharpe: {results['avg_sharpe']:.2f}")
        print(f"  Robust: {results['robust']}")

    def test_recommendation_logic(self):
        """Test that recommendation logic is sound"""
        # Create a validator
        result = self.validator.validate_strategy(
            use_synthetic=True,
            synthetic_days=30
        )

        assessment = result['assessment']
        recommendation = assessment['recommendation']

        # Recommendation should be one of the valid options
        self.assertIn(recommendation, ['GO', 'CAUTIOUS GO', 'NO GO'])

        # If recommendation is GO, pass rate should be high
        if recommendation == 'GO':
            self.assertGreaterEqual(assessment['pass_rate'], 60)

        # If profitable, return should be positive
        if assessment['criteria']['profitable']['passed']:
            self.assertGreater(result['result'].total_return, 0)

        print(f"✓ Recommendation logic is sound")
        print(f"  Recommendation: {recommendation}")

    def test_data_period_tracking(self):
        """Test that data period is tracked correctly"""
        result = self.validator.validate_strategy(
            use_synthetic=True,
            synthetic_days=30
        )

        # Check data period is tracked
        self.assertIn('data_period', result)
        self.assertIn('data_points', result)

        start, end = result['data_period']
        self.assertIsNotNone(start)
        self.assertIsNotNone(end)
        self.assertGreater(end, start)

        print(f"✓ Data period tracking works")
        print(f"  Period: {start} to {end}")
        print(f"  Data points: {result['data_points']}")


def run_tests():
    """Run all tests with detailed output"""
    print("=" * 70)
    print("BACKTEST VALIDATION SYSTEM TESTS")
    print("=" * 70)
    print()

    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBacktestValidation)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print()
        print("✅ All backtest validation tests passed!")
        return 0
    else:
        print()
        print("❌ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(run_tests())
