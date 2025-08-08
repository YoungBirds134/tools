#!/bin/bash
# Python Version Checker for FC Trading API

echo "🐍 Python Version Checker"
echo "========================="
echo ""

# Check available Python versions
echo "Available Python versions:"
for cmd in python3.11 python3.10 python3.9 python3 python; do
    if command -v $cmd &> /dev/null; then
        version=$($cmd --version 2>&1)
        echo "  ✅ $cmd: $version"
    fi
done

echo ""
echo "Virtual Environment Status:"
if [[ -d "venv" ]]; then
    if [[ -f "venv/bin/python" ]]; then
        venv_version=$(venv/bin/python --version 2>&1)
        echo "  📦 venv Python: $venv_version"
        echo "  📁 venv path: $(pwd)/venv"
        
        # Check if activated
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            echo "  ✅ Virtual environment is activated"
            echo "  🔗 Active venv: $VIRTUAL_ENV"
        else
            echo "  ⚠️  Virtual environment exists but not activated"
            echo "  💡 Activate with: source venv/bin/activate"
        fi
    else
        echo "  ❌ Virtual environment corrupted (missing python)"
    fi
else
    echo "  ❌ No virtual environment found"
    echo "  💡 Create with: python3 -m venv venv"
fi

echo ""
echo "Recommendations:"
if [[ -d "venv" ]] && [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "  🔄 Activate your environment: source venv/bin/activate"
elif [[ ! -d "venv" ]]; then
    echo "  🆕 Run setup: ./setup_fc_trading.sh"
else
    echo "  ✅ Everything looks good!"
fi
