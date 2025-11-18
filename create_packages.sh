#!/usr/bin/env bash
#
# Package both versions of AI Trading Tool
#
# This script creates two tar.gz archives:
# 1. ai-trading-llm-powered-v1.tar.gz (LLM-powered version)
# 2. ai-trading-claude-skill-v2.tar.gz (Claude Skill version)
#

set -e

echo "================================"
echo "AI Trading Tool - Packaging"
echo "================================"
echo ""

# Create temporary directories
TEMP_DIR="./packaging_temp"
mkdir -p "$TEMP_DIR"

echo "[1/4] Preparing Version 1 (LLM-Powered)..."

# Version 1: LLM-Powered
V1_DIR="$TEMP_DIR/ai-trading-llm-powered-v1"
mkdir -p "$V1_DIR"

# Copy core files
cp -r cryptocurrency-trader-skill/scripts "$V1_DIR/"
cp cryptocurrency-trader-skill/llm_trading_assistant.py "$V1_DIR/"
cp cryptocurrency-trader-skill/requirements.txt "$V1_DIR/"
cp VERSION1_README.md "$V1_DIR/README.md"

# Copy documentation
cp TASK1_FEATURE_ANALYSIS.md "$V1_DIR/FEATURE_ANALYSIS.md"
cp TASK2_RESEARCH_AND_ENHANCEMENT_PLAN.md "$V1_DIR/RESEARCH_PLAN.md"
cp TASK3_IMPLEMENTATION_COMPLETE.md "$V1_DIR/IMPLEMENTATION.md"

# Create LLM requirements
cat > "$V1_DIR/requirements-llm.txt" << 'EOF'
# Core dependencies
pandas>=1.3.0
numpy>=1.21.0
ccxt>=4.0.0
scipy>=1.7.0
scikit-learn>=1.0.0
ta>=0.10.0

# LLM dependencies (choose one or both)
openai>=1.0.0        # For OpenAI GPT-4
anthropic>=0.18.0    # For Anthropic Claude
EOF

echo "✓ Version 1 prepared"

echo "[2/4] Preparing Version 2 (Claude Skill)..."

# Version 2: Claude Skill
V2_DIR="$TEMP_DIR/ai-trading-claude-skill-v2"
mkdir -p "$V2_DIR"

# Copy core files
cp -r cryptocurrency-trader-skill/scripts "$V2_DIR/"
cp cryptocurrency-trader-skill/skill.py "$V2_DIR/"
cp cryptocurrency-trader-skill/__main__.py "$V2_DIR/"
cp cryptocurrency-trader-skill/run.sh "$V2_DIR/"
cp cryptocurrency-trader-skill/requirements.txt "$V2_DIR/"
cp cryptocurrency-trader-skill/SKILL.md "$V2_DIR/"
cp VERSION2_README.md "$V2_DIR/README.md"

# Copy documentation
cp TASK1_FEATURE_ANALYSIS.md "$V2_DIR/FEATURE_ANALYSIS.md"
cp TASK2_RESEARCH_AND_ENHANCEMENT_PLAN.md "$V2_DIR/RESEARCH_PLAN.md"
cp TASK3_IMPLEMENTATION_COMPLETE.md "$V2_DIR/IMPLEMENTATION.md"

# Make scripts executable
chmod +x "$V2_DIR/skill.py"
chmod +x "$V2_DIR/run.sh"

echo "✓ Version 2 prepared"

echo "[3/4] Creating archives..."

# Create archives
cd "$TEMP_DIR"

# Version 1
tar -czf ../ai-trading-llm-powered-v1.tar.gz ai-trading-llm-powered-v1/
echo "✓ Created: ai-trading-llm-powered-v1.tar.gz"

# Version 2
tar -czf ../ai-trading-claude-skill-v2.tar.gz ai-trading-claude-skill-v2/
echo "✓ Created: ai-trading-claude-skill-v2.tar.gz"

cd ..

echo "[4/4] Cleaning up..."
rm -rf "$TEMP_DIR"
echo "✓ Cleanup complete"

echo ""
echo "================================"
echo "Packaging Complete!"
echo "================================"
echo ""
echo "Created archives:"
echo "  📦 ai-trading-llm-powered-v1.tar.gz (Version 1 - LLM-Powered)"
echo "  📦 ai-trading-claude-skill-v2.tar.gz (Version 2 - Claude Skill)"
echo ""
echo "Extract and use:"
echo "  Version 1: tar -xzf ai-trading-llm-powered-v1.tar.gz"
echo "  Version 2: tar -xzf ai-trading-claude-skill-v2.tar.gz"
echo ""
echo "See README.md in each archive for usage instructions."
echo ""
