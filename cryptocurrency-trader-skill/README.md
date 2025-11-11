# Cryptocurrency Trading Agent - Claude Skill

> AI trading agent for cryptocurrency markets with hallucination prevention, technical analysis, and risk management

## Overview

This is a Claude AI skill that provides comprehensive cryptocurrency trading analysis with built-in safeguards against common AI mistakes and trading psychology traps.

**Key Features:**
- Real-time technical analysis across multiple timeframes
- Market scanning of 30+ cryptocurrencies
- Anti-hallucination data validation
- Automated position sizing and risk management
- Circuit breaker system for safety
- Beginner-friendly interface

## Installation

### For Claude AI Users

1. Copy the entire `cryptocurrency-trader-skill` folder to your Claude skills directory
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. The skill will appear automatically in your Claude interface

### Required Dependencies

- Python 3.8+
- ccxt >= 4.0.0
- pandas >= 2.0.0
- numpy >= 1.24.0

## Usage

The skill is invoked when you ask Claude about cryptocurrency trading analysis. Examples:

- "Analyze BTC/USDT for trading opportunities"
- "Scan the crypto market for the best trades right now"
- "What's the technical analysis for ETH/USDT?"
- "Find me the top 5 trading opportunities in cryptocurrency"

## Structure

```
cryptocurrency-trader-skill/
├── SKILL.md                    # Claude skill definition (main entry point)
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── scripts/
│   └── trading_agent.py        # Main trading agent implementation (518 lines)
├── tests/
│   └── test_trading_agent.py   # Comprehensive test suite
└── resources/
    ├── user-guide.md           # Complete user documentation
    ├── protocol.md             # Technical analysis protocol
    ├── psychology.md           # Trading psychology reference
    └── optimization.md         # Performance optimization guide
```

## What Makes This Special

### Anti-Hallucination Framework
- Validates all market data automatically
- Rejects stale data (>5 minutes old)
- No false precision (confidence rounded to whole numbers)
- Explicit "UNKNOWN" instead of guessing

### Safety Circuits
8 mandatory circuit breakers that prevent dangerous trades:
- Low confidence signals (< 40%)
- Poor risk/reward ratios (< 1.5:1)
- Stale or invalid data
- Insufficient timeframe confirmation

### Beginner-Friendly
- Plain language explanations
- Guided step-by-step workflow
- Risk warnings prominently displayed
- Position sizing automated (2% max risk rule)

## Quick Start (Standalone Usage)

```python
from scripts.trading_agent import TradingAgent

# Initialize with your balance
agent = TradingAgent(balance=10000)

# Analyze a specific coin
analysis = agent.analyze_opportunity('BTC/USDT', timeframes=['15m', '1h', '4h'])
agent.display_opportunity(analysis)

# Or scan the entire market
top_5 = agent.scan_market()
for i, opp in enumerate(top_5, 1):
    agent.display_opportunity(opp, rank=i)
```

## Testing

```bash
python tests/test_trading_agent.py
```

Expected: 2-3/3 tests passed (network test may fail in restricted environments)

## Documentation

- **SKILL.md** - Claude skill instructions (how Claude uses this skill)
- **resources/user-guide.md** - Complete feature documentation
- **resources/protocol.md** - Technical analysis protocol details
- **resources/psychology.md** - 15 trading psychology biases addressed
- **resources/optimization.md** - Performance improvement recommendations

## Market Coverage

**30+ Cryptocurrencies across 6 categories:**
- Major Coins: BTC, ETH, BNB, SOL, XRP
- AI Tokens: RENDER, FET, AGIX, OCEAN, TAO
- Layer 1: ADA, AVAX, DOT, ATOM
- Layer 2: MATIC, ARB, OP
- DeFi: UNI, AAVE, LINK, MKR
- Meme: DOGE, SHIB, PEPE

## Technical Indicators

- RSI (Relative Strength Index)
- MACD (Moving Average Convergence Divergence)
- ATR (Average True Range)
- Bollinger Bands
- Multi-timeframe Consensus (15m, 1h, 4h)

## Important Disclaimers

**This is NOT financial advice.** This tool:
- Analyzes market data using technical indicators
- Enforces risk management rules
- Prevents common trading mistakes

But markets are unpredictable and:
- Even perfect analysis can be wrong
- You are responsible for your trading decisions
- Start small and never risk more than you can afford to lose
- Always use stop losses to protect your capital
- Past performance does not guarantee future results

## Version

**v1.0.0** - Production release with comprehensive anti-hallucination framework

## License

MIT License - Use freely, no warranties provided

## Support

For issues or questions:
1. Check the user-guide.md for detailed documentation
2. Review test results for diagnostics
3. Verify exchange connectivity and data freshness

---

**Built for Claude AI Skills** - Designed to work seamlessly with Claude's agentic capabilities while maintaining strict safety standards.
