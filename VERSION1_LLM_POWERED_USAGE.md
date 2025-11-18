# Version 1: LLM-Powered AI Trading Tool - Usage Guide

## Overview

The LLM-Powered AI Trading Tool is a conversational cryptocurrency trading assistant that combines advanced technical analysis with natural language interaction. It provides educational explanations, personalized recommendations, and interactive guidance for cryptocurrency trading.

**Key Features:**
- 🤖 Natural language conversation interface
- 📊 12-stage comprehensive trading analysis
- 📚 Educational explanations of complex concepts
- 🎯 Personalized trading recommendations
- ⚖️ Risk-aware decision making
- 🔄 Adaptive learning from trade outcomes
- 🌐 Multi-exchange data aggregation
- 📈 Market context awareness

**Target Reliability:** 9.5/10

---

## Quick Start

### 1. Installation

```bash
# Extract the archive
tar -xzf ai-trading-llm-powered-v1.tar.gz
cd ai-trading-llm-powered-v1

# Install dependencies
pip install -r requirements.txt

# Install LLM provider (choose one or both)
pip install openai      # For OpenAI GPT-4
pip install anthropic   # For Anthropic Claude
```

### 2. Set Up API Key

**For OpenAI:**
```bash
export OPENAI_API_KEY="sk-..."
```

**For Anthropic Claude:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### 3. Run Interactive Mode

```bash
# With OpenAI GPT-4
python llm_trading_assistant.py --interactive --provider openai

# With Anthropic Claude
python llm_trading_assistant.py --interactive --provider anthropic
```

---

## Usage Modes

### Interactive Chat Mode

The most natural way to use the assistant - have a conversation!

```bash
python llm_trading_assistant.py --interactive --provider openai
```

**Example Conversation:**

```
You: Should I buy Bitcoin right now? I have $10,000 to invest.