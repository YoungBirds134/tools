#!/bin/bash

# Test script để demo scenario với Python 3.9
echo "🧪 Testing Python 3.9 scenario..."

# Tạo một venv giả với Python 3.9 version
echo "Creating fake Python 3.9 venv for testing..."

# Backup current venv if exists
if [[ -d "venv" ]]; then
    echo "Backing up current venv..."
    mv venv venv_backup_$(date +%s)
fi

# Create a fake venv structure with Python 3.9 version
mkdir -p venv/bin
mkdir -p venv/lib/python3.9/site-packages

# Create a fake python executable that reports version 3.9
cat > venv/bin/python << 'EOF'
#!/bin/bash
if [[ "$1" == "--version" ]]; then
    echo "Python 3.9.18"
else
    echo "This is a fake Python 3.9 for testing"
    echo "Arguments: $@"
fi
EOF
chmod +x venv/bin/python

# Create a fake activate script
cat > venv/bin/activate << 'EOF'
# This is a fake activate script for testing
export VIRTUAL_ENV="/Users/huynt/Downloads/16072025/fc-trading.py/venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"
unset PYTHON_HOME
echo "Activated fake Python 3.9 environment"
EOF

echo "✅ Fake Python 3.9 venv created"
echo ""
echo "Now run: ./setup_fc_trading.sh"
echo "You should see the Python version mismatch detection and get prompted to recreate the environment"
echo ""
echo "To restore original venv later:"
echo "  rm -rf venv"
echo "  mv venv_backup_* venv  # if backup exists"
