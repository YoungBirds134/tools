#!/bin/bash
# Quick activation script for FC Trading API

echo "🐍 Activating FC Trading virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""
echo "Available commands:"
echo "  ./start.sh dev    - Start development server"
echo "  ./start.sh bot    - Start Telegram bot only"
echo "  ./start.sh test   - Run tests"
echo "  deactivate        - Exit virtual environment"
