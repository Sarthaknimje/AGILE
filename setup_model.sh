#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up ML model and data..."

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🐍 Activating virtual environment..."
    source .venv/bin/activate
fi

# Generate data if it doesn't exist
if [ ! -f "data/processed/portfolios.csv" ]; then
    echo "📊 Generating portfolio data..."
    python -m app.data.generate
else
    echo "✅ Portfolio data already exists"
fi

# Train model
echo "🤖 Training ML model..."
python -m app.models.train

echo "✅ Model setup complete!"
