---
name: cryptocurrency-trader
description: AI trading agent for cryptocurrency markets with hallucination prevention, technical analysis, market scanning, and risk management. Analyzes 30+ cryptocurrencies, provides entry/exit signals with confidence levels, and enforces strict safety circuits to prevent common trading mistakes.
---

# Cryptocurrency Trading Agent Skill

## Overview

This skill provides a comprehensive AI trading agent for cryptocurrency markets that prevents hallucinations, identifies trading opportunities automatically, and enforces strict risk management rules.

**Core Capabilities:**
- Real-time technical analysis across multiple timeframes (15m, 1h, 4h)
- Market scanning of 30+ cryptocurrencies in 6 categories
- Anti-hallucination data validation framework
- Automated position sizing and risk management
- Circuit breaker system to prevent dangerous trades
- Beginner-friendly explanations and guidance

## When to Use This Skill

Use this skill when the user wants to:
- Analyze specific cryptocurrency trading pairs (e.g., BTC/USDT, ETH/USDT)
- Find the best trading opportunities across the crypto market
- Get technical analysis with entry, stop loss, and take profit levels
- Understand market conditions with risk/reward ratios
- Receive trading recommendations with confidence levels
- Learn about trading psychology and common mistakes

## Prerequisites

Before using this skill, ensure:
1. Python environment is available with required packages: ccxt, pandas, numpy
2. Internet connection for real-time market data from exchanges
3. User's account balance is known for position sizing

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Use This Skill

### Step 1: Understand User Intent

Ask the user to clarify:
- What is your trading account balance? (needed for position sizing)
- Do you want to analyze a specific cryptocurrency OR scan the entire market?
- If specific: Which trading pair? (e.g., BTC/USDT, ETH/USDT, SOL/USDT)

### Step 2: Run the Trading Agent

Execute the trading agent script:

```bash
cd cryptocurrency-trader-skill
python scripts/trading_agent.py
```

Or use programmatically:

```python
from scripts.trading_agent import TradingAgent

# Initialize with user's balance
agent = TradingAgent(balance=10000)

# Option A: Analyze specific coin
analysis = agent.analyze_opportunity(
    symbol='BTC/USDT',
    timeframes=['15m', '1h', '4h']
)
agent.display_opportunity(analysis)

# Option B: Scan entire market for top opportunities
top_opportunities = agent.scan_market()
for i, opp in enumerate(top_opportunities, 1):
    agent.display_opportunity(opp, rank=i)
```

### Step 3: Interpret and Explain Results

The agent provides structured analysis with:

**Trading Signal:**
- Action: LONG (buy), SHORT (sell), or WAIT (no clear opportunity)
- Confidence Level: 0-100% (realistic, not overconfident)
- Entry Price: Recommended entry point
- Stop Loss: Where to exit if trade goes wrong (protects capital)
- Take Profit: Target profit level
- Risk/Reward Ratio: How much you can make vs. how much you risk

**Position Sizing:**
- Amount to trade based on 2% max risk rule
- Dollar amount and coin quantity

**Safety Warnings:**
- Circuit breaker blocks (mandatory reasons NOT to trade)
- Warning flags (cautions but doesn't block trade)

### Step 4: Provide Beginner-Friendly Explanations

Always explain results in simple terms:

- **LONG** = "Buy now, sell higher later for profit"
- **SHORT** = "Sell now, buy back cheaper later for profit"
- **WAIT** = "No clear opportunity right now, patience is key"
- **Stop Loss** = "Automatic exit to limit your loss if wrong"
- **Take Profit** = "Automatic exit to lock in profits"
- **Confidence** = "How strong the signal is, NOT a guarantee"
- **Risk/Reward** = "For every $1 you risk, how much you could make"

### Step 5: Emphasize Risk Warnings

ALWAYS include these critical reminders:

- Markets are unpredictable - even perfect analysis can be wrong
- Start with small amounts to learn
- Never risk more than 2% of account per trade (enforced automatically)
- Always use stop losses to protect your capital
- This is analysis, NOT financial advice
- Past performance does NOT guarantee future results

## Anti-Hallucination Framework

The skill enforces strict validation to prevent false data:

**Data Validation Checks:**
- No negative or zero prices
- OHLC logic verification (High ≥ Low, Open, Close)
- Volume must be positive
- Data freshness (rejects data >5 minutes old)
- No missing values
- Mathematical verification of all calculations

**Precision Control:**
- Confidence levels rounded to whole numbers (no false precision like 87.4532%)
- Prices formatted appropriately (no excessive decimals)
- Explicit "UNKNOWN" instead of guessing

**Circuit Breakers** (8 mandatory blocks):
1. No clear signal (action = WAIT)
2. Confidence < 40%
3. Risk/reward < 1.5:1
4. Insufficient timeframes (< 2)
5. Stale data (> 5 minutes)
6. Invalid price data
7. OHLC logic violations
8. Missing critical indicators

## Market Categories

The agent analyzes 30+ cryptocurrencies across 6 categories:

1. **Major Coins**: BTC, ETH, BNB, SOL, XRP
2. **AI Tokens**: RENDER, FET, AGIX, OCEAN, TAO
3. **Layer 1**: ADA, AVAX, DOT, ATOM
4. **Layer 2**: MATIC, ARB, OP
5. **DeFi**: UNI, AAVE, LINK, MKR
6. **Meme**: DOGE, SHIB, PEPE

## Technical Indicators Used

- **RSI** (Relative Strength Index): Measures overbought/oversold conditions
- **MACD** (Moving Average Convergence Divergence): Identifies trend direction
- **ATR** (Average True Range): Measures volatility for stop loss placement
- **Bollinger Bands**: Identifies price extremes and volatility
- **Multi-timeframe Consensus**: Confirms signals across 15m, 1h, 4h timeframes

## Output Format

Present results clearly with:

```
🔍 Analyzing [SYMBOL]...
💰 CURRENT PRICE: $[price]
📈 RECOMMENDATION: [LONG/SHORT/WAIT] at $[price]

🎯 ACTION: [LONG/SHORT/WAIT]
📊 CONFIDENCE: [X]% (NOT a guarantee)
💵 ENTRY PRICE: $[price]
🛑 STOP LOSS: $[price]
🎁 TAKE PROFIT: $[price]
⚖️ RISK/REWARD: 1:[ratio]

💼 POSITION SIZING (based on $[balance] balance):
- Risk Amount: $[amount] (2% of balance)
- Position Size: $[amount] ([quantity] coins)

⛔ CIRCUIT BREAKERS: [any blocks]
⚠️ WARNINGS: [any warnings]
```

## Common User Questions

**Q: What confidence level should I look for?**
A: 60%+ is moderate, 70%+ is strong. Avoid anything >90% (unrealistic). Never trade below 40%.

**Q: What's a good risk/reward ratio?**
A: Minimum 1.5:1 (make $1.50 for every $1 risked). Prefer 2:1 or better.

**Q: How much should I trade?**
A: The agent enforces 2% max risk per trade and 10% max position size automatically.

**Q: What if it shows WAIT?**
A: That's normal! Most of the time, the best action is to wait for clear opportunities.

**Q: Can I trust the analysis?**
A: Use it as one input among many. Do your own research, start small, and never risk money you can't afford to lose.

## Resources

For detailed technical information, refer to:
- `resources/user-guide.md` - Complete user documentation
- `resources/protocol.md` - Technical analysis protocol
- `resources/psychology.md` - Trading psychology reference
- `resources/optimization.md` - Performance optimization guide
- `scripts/trading_agent.py` - Main agent implementation (518 lines)
- `tests/test_trading_agent.py` - Comprehensive test suite

## Testing

Run tests to verify functionality:

```bash
python tests/test_trading_agent.py
```

Expected: 2-3/3 tests passed (network test may fail in restricted environments)

## Safety Reminders

This skill helps make better decisions but:
- YOU are responsible for your trading
- Start small and learn
- Markets are unpredictable
- This is NOT financial advice
- Use stop losses always
- Never risk more than you can afford to lose

## Version

v1.0.0 - Production-ready with comprehensive anti-hallucination framework and beginner-friendly interface
