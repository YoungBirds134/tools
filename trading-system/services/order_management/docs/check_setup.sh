#!/bin/bash
# Verify FC Trading setup

source venv/bin/activate

echo "🔍 FC Trading Setup Verification"
echo "================================"
echo ""

echo "Python Environment:"
echo "  Virtual Env: $VIRTUAL_ENV"
echo "  Python: $(which python)"
echo "  Pip: $(which pip)"
echo ""

echo "Key Dependencies:"
python -c "
packages = ['fastapi', 'uvicorn', 'telegram', 'redis', 'celery', 'pydantic']
for pkg in packages:
    try:
        module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        print(f'  ✅ {pkg}: {version}')
    except ImportError:
        print(f'  ❌ {pkg}: not installed')
"

echo ""
echo "Configuration:"
if [ -f ".env" ]; then
    echo "  ✅ .env file exists"
    if grep -q "your-bot-token-here" .env; then
        echo "  ⚠️  Bot token needs to be updated"
    else
        echo "  ✅ Bot token configured"
    fi
else
    echo "  ❌ .env file missing"
fi

echo ""
echo "Project Structure:"
dirs=("app" "app/telegram" "app/routers" "tests")
for dir in "${dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir/"
    else
        echo "  ❌ $dir/ missing"
    fi
done
