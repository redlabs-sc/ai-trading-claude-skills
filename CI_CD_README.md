# CI/CD Pipeline Documentation

## Overview

Automated testing and quality assurance pipeline for AI Trading Claude Skills.

## Components

### 1. GitHub Actions Workflow (`.github/workflows/ci.yml`)

Automatically runs on:
- Push to `main`, `develop`, or `claude/**` branches
- Pull requests to `main` or `develop`

**Jobs:**

#### Test Suite (Matrix: Python 3.9, 3.10, 3.11)
- ✅ GBM systematic bias fix tests
- ✅ Division by zero protection tests
- ✅ Benford's Law extraction tests
- ✅ Backtesting framework tests
- ✅ Configuration system tests

#### Code Quality
- **Black**: Code formatting check
- **Flake8**: Linting and style guide enforcement
- **Pylint**: Advanced static analysis

#### Security Scan
- **Bandit**: Security vulnerability scanning
- **Safety**: Known dependency vulnerability checks

#### Build Validation
- YAML configuration validation
- Build summary and reporting

### 2. Local Test Runner (`run_tests.sh`)

Runs all test suites locally before pushing:

```bash
./run_tests.sh
```

**Features:**
- Color-coded output
- Progress tracking
- Detailed summary
- Exit codes (0 = pass, 1 = fail)

### 3. Pytest Configuration (`pytest.ini`)

Configured for:
- Test discovery patterns
- Organized test markers
- Coverage reporting (optional)
- Python 3.9+ requirement

## Usage

### Running Tests Locally

**All tests:**
```bash
./run_tests.sh
```

**Individual test suites:**
```bash
python test_gbm_fix.py
python test_div_zero_simple.py
python test_benford_fix.py
python test_backtest_framework.py
python test_config_system.py
```

**With pytest (if installed):**
```bash
pip install pytest
pytest -v
```

### CI/CD Pipeline Status

The pipeline runs automatically on every push/PR. Check status at:
```
https://github.com/YOUR_USERNAME/ai-trading-claude-skills/actions
```

### Test Coverage

Current coverage: **50+ individual test cases** across 5 suites

| Test Suite | Tests | Status |
|------------|-------|--------|
| GBM Fix | 3 | ✅ |
| Division by Zero | 5 | ✅ |
| Benford's Law | 26 | ✅ |
| Backtesting Framework | 6 | ✅ |
| Configuration System | 10 | ✅ |
| **Total** | **50+** | **✅** |

## Adding New Tests

### 1. Create Test File

```python
#!/usr/bin/env python3
"""
Test description
"""

def test_something():
    """Test function description"""
    # Test implementation
    assert True
    return True

if __name__ == '__main__':
    # Run tests
    result = test_something()
    sys.exit(0 if result else 1)
```

### 2. Add to Test Runner

Edit `run_tests.sh`:

```bash
run_test "test_new_feature.py" "New Feature Tests"
```

### 3. Add to CI Workflow

Edit `.github/workflows/ci.yml`:

```yaml
- name: Run new feature tests
  run: |
    python test_new_feature.py
```

## Test Markers (for pytest)

Organize tests with markers:

```python
import pytest

@pytest.mark.critical
def test_critical_function():
    # Critical bug fix test
    pass

@pytest.mark.feature
def test_new_feature():
    # Feature test
    pass

@pytest.mark.slow
def test_long_running():
    # Slow test
    pass
```

Run specific markers:
```bash
pytest -m critical  # Only critical tests
pytest -m "not slow"  # Skip slow tests
```

## Quality Standards

### Code must pass:
- ✅ All test suites (50+ tests)
- ✅ Black formatting check
- ✅ Flake8 linting (no syntax errors)
- ✅ Pylint static analysis
- ✅ Bandit security scan
- ✅ Configuration validation

### Before Pushing:

1. **Run tests locally:**
   ```bash
   ./run_tests.sh
   ```

2. **Format code:**
   ```bash
   pip install black
   black cryptocurrency-trader-skill/scripts/
   ```

3. **Check linting:**
   ```bash
   pip install flake8
   flake8 cryptocurrency-trader-skill/scripts/
   ```

4. **Push changes:**
   ```bash
   git push
   ```

5. **Check CI status:**
   - Wait for GitHub Actions to complete
   - Fix any failures
   - Merge when all checks pass ✅

## Troubleshooting

### Tests fail locally but pass in CI
- Check Python version (CI tests 3.9, 3.10, 3.11)
- Check dependencies: `pip install -r requirements.txt`
- Check working directory

### Tests pass locally but fail in CI
- Check for missing dependencies in `requirements.txt`
- Check for hardcoded paths
- Check for environment-specific code

### CI workflow not triggering
- Check branch name matches patterns (`main`, `develop`, `claude/**`)
- Check `.github/workflows/ci.yml` syntax
- Check repository Actions settings (must be enabled)

## Performance

**CI Pipeline Duration:**
- Test Suite: ~2-3 minutes per Python version
- Code Quality: ~1 minute
- Security Scan: ~1 minute
- Total: ~10-15 minutes for full pipeline

**Local Test Runner:**
- All tests: ~30-60 seconds
- Individual suite: ~5-15 seconds

## Future Enhancements

### Planned:
- [ ] Coverage reporting with codecov.io
- [ ] Performance benchmarks
- [ ] Integration tests with live data
- [ ] Automated dependency updates (Dependabot)
- [ ] Docker containerization for tests
- [ ] Deploy previews for PRs

### Configuration Options:

**Enable coverage reporting in pytest.ini:**
```ini
addopts =
    --cov=cryptocurrency-trader-skill/scripts
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

**Run with coverage:**
```bash
pip install pytest-cov
pytest --cov
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [Pylint Documentation](https://pylint.pycqa.org/)

## Support

For CI/CD issues:
1. Check GitHub Actions logs
2. Run `./run_tests.sh` locally
3. Review this documentation
4. Check individual test files for details

---

**Status:** ✅ All systems operational
**Last Updated:** 2025-01-12
