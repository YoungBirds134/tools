# Python Virtual Environment Guide

## 📋 Tổng quan về Virtual Environment

Virtual Environment (môi trường ảo) là một công cụ quan trọng trong Python giúp tách biệt các dependencies của các project khác nhau. Điều này đảm bảo rằng các package và phiên bản khác nhau không xung đột với nhau.

## 🎯 Tại sao cần Virtual Environment?

### Vấn đề không có Virtual Environment:
```bash
# Không có venv - Tất cả packages cài global
pip install fastapi==0.104.1    # Project A cần FastAPI 0.104.1
pip install fastapi==0.95.0     # Project B cần FastAPI 0.95.0 → Conflict!
```

### Giải pháp với Virtual Environment:
```bash
# Project A có venv riêng
cd project-a && source venv/bin/activate
pip install fastapi==0.104.1

# Project B có venv riêng  
cd project-b && source venv/bin/activate
pip install fastapi==0.95.0
```

## 🛠️ Hướng dẫn tạo Virtual Environment

### Method 1: Sử dụng `venv` (Built-in Python 3.3+)

#### Tạo Virtual Environment:
```bash
# Tạo venv mới
python -m venv venv

# Hoặc với tên cụ thể
python -m venv my_project_env

# Với Python version cụ thể (nếu có nhiều version)
python3.11 -m venv venv
```

#### Kích hoạt Virtual Environment:

**Trên macOS/Linux:**
```bash
# Kích hoạt venv
source venv/bin/activate

# Verify activation (should show venv path)
which python
which pip
```

**Trên Windows:**
```cmd
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

**Dấu hiệu đã activate thành công:**
```bash
# Terminal prompt sẽ hiển thị (venv)
(venv) username@computer:~/project$ 
```

#### Tắt Virtual Environment:
```bash
# Tắt venv (từ bất kỳ directory nào)
deactivate
```

### Method 2: Sử dụng `conda` (Anaconda/Miniconda)

```bash
# Tạo conda environment
conda create -n fc_trading python=3.11

# Kích hoạt
conda activate fc_trading

# Tắt
conda deactivate

# Xóa environment
conda remove -n fc_trading --all
```

### Method 3: Sử dụng `virtualenv` (Third-party tool)

```bash
# Cài đặt virtualenv
pip install virtualenv

# Tạo venv
virtualenv venv

# Kích hoạt (giống như venv)
source venv/bin/activate
```

## 🚀 Setup cho FC Trading Project

### Quick Setup Script

Tạo file `setup_venv.sh`:
```bash
#!/bin/bash

echo "🐍 Setting up Python Virtual Environment for FC Trading API..."

# Check Python version
python_version=$(python3 --version 2>&1)
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

echo "✅ Setup completed!"
echo ""
echo "To activate the environment manually:"
echo "source venv/bin/activate"
echo ""
echo "To start the application:"
echo "./start.sh dev"
```

### Manual Setup Steps

```bash
# 1. Navigate to project directory
cd fc-trading.py

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Upgrade pip
pip install --upgrade pip

# 5. Install project dependencies
pip install -r requirements.txt

# 6. Verify installation
pip list
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
```

## 🔧 Virtual Environment Management

### Kiểm tra Virtual Environment

```bash
# Check if venv is active
echo $VIRTUAL_ENV

# List installed packages
pip list

# Check specific package
pip show fastapi

# Generate requirements file
pip freeze > requirements.txt

# Show environment info
python -m site
```

### Package Management trong Virtual Environment

```bash
# Install specific version
pip install fastapi==0.104.1

# Install from requirements
pip install -r requirements.txt

# Install with extras
pip install "fastapi[all]"

# Upgrade package
pip install --upgrade fastapi

# Uninstall package
pip uninstall fastapi

# Install development dependencies
pip install -e .
```

### Dependencies Management

```bash
# Generate exact requirements (recommended for production)
pip freeze > requirements-exact.txt

# Generate loose requirements (recommended for development)
pip install pipreqs
pipreqs . --force

# Check for outdated packages
pip list --outdated

# Upgrade all packages (careful!)
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip install -U
```

## 🐛 Troubleshooting Virtual Environment

### Common Issues và Solutions

#### Issue 1: `python: command not found`
```bash
# Solution: Check Python installation
which python3
python3 --version

# Or install Python
# macOS: brew install python
# Ubuntu: sudo apt install python3 python3-pip
```

#### Issue 2: `Permission denied` khi tạo venv
```bash
# Solution: Check permissions
ls -la $(which python3)

# Or use user directory
python3 -m venv --user venv
```

#### Issue 3: `pip: command not found` trong venv
```bash
# Solution: Reinstall pip trong venv
python -m ensurepip --upgrade
python -m pip install --upgrade pip
```

#### Issue 4: Package conflicts
```bash
# Solution: Clean install
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Issue 5: `ModuleNotFoundError` sau khi activate
```bash
# Check Python path
python -c "import sys; print(sys.path)"

# Verify venv activation
which python
which pip

# Reinstall requirements
pip install -r requirements.txt
```

### Virtual Environment Best Practices

#### 1. Naming Convention
```bash
# Good names
python3 -m venv venv          # Standard
python3 -m venv .venv         # Hidden folder
python3 -m venv env           # Alternative

# Bad names
python3 -m venv my-env        # Avoid hyphens
python3 -m venv 123env        # Don't start with numbers
```

#### 2. .gitignore for Virtual Environment
```gitignore
# Virtual Environment
venv/
.venv/
env/
ENV/
venv.bak/
```

#### 3. Requirements Files Organization
```bash
# Development
requirements-dev.txt    # All dependencies including dev tools
requirements.txt        # Production dependencies only
requirements-test.txt   # Test dependencies

# Example requirements-dev.txt
-r requirements.txt
black==23.11.0
pytest==7.4.3
mypy==1.7.1
```

#### 4. Environment Variables in Virtual Environment
```bash
# Create .env file
echo "ENVIRONMENT=development" > .env
echo "DEBUG=true" >> .env

# Load trong activate script
echo 'export $(cat .env | xargs)' >> venv/bin/activate
```

## 🚀 FC Trading Specific Setup

### Complete Setup Script cho FC Trading

```bash
#!/bin/bash
# File: setup_fc_trading.sh

set -e

echo "🚀 FC Trading API - Complete Environment Setup"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
info() { echo -e "${BLUE}[STEP]${NC} $1"; }

# Step 1: Check Python
info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3.11+ first:"
    echo "  macOS: brew install python"
    echo "  Ubuntu: sudo apt install python3 python3-pip"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2)
log "Python version: $python_version"

# Step 2: Create Virtual Environment
info "Creating virtual environment..."
if [ -d "venv" ]; then
    warn "Virtual environment already exists"
    read -p "Do you want to recreate it? (y/N): " recreate
    if [[ $recreate == "y" || $recreate == "Y" ]]; then
        rm -rf venv
        python3 -m venv venv
        log "Virtual environment recreated"
    fi
else
    python3 -m venv venv
    log "Virtual environment created"
fi

# Step 3: Activate Virtual Environment
info "Activating virtual environment..."
source venv/bin/activate
log "Virtual environment activated"

# Step 4: Upgrade pip
info "Upgrading pip..."
pip install --upgrade pip
pip_version=$(pip --version | cut -d' ' -f2)
log "pip version: $pip_version"

# Step 5: Install Requirements
info "Installing FC Trading dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    log "Dependencies installed successfully"
else
    warn "requirements.txt not found"
fi

# Step 6: Setup Environment File
info "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.production" ]; then
        cp .env.production .env
        warn "Please update .env with your actual credentials"
    else
        warn ".env.production template not found"
    fi
fi

# Step 7: Verify Installation
info "Verifying installation..."
python -c "
try:
    import fastapi
    import uvicorn
    import telegram
    print('✅ FastAPI version:', fastapi.__version__)
    print('✅ Uvicorn installed')
    print('✅ Telegram Bot library installed')
    print('✅ All core dependencies verified')
except ImportError as e:
    print('❌ Missing dependency:', e)
    exit(1)
"

# Step 8: Setup Complete
echo ""
log "🎉 Setup completed successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env with your credentials:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - FC_USERNAME"
echo "   - FC_PASSWORD"
echo ""
echo "2. Start the application:"
echo "   ./start.sh dev"
echo ""
echo "3. Or activate manually:"
echo "   source venv/bin/activate"
echo "   python run.py"
```

### Daily Workflow

```bash
# 1. Activate environment (every session)
source venv/bin/activate

# 2. Check for updates
pip list --outdated

# 3. Start development
./start.sh dev

# 4. Run tests
./start.sh test

# 5. Deactivate when done
deactivate
```

## 📚 Advanced Virtual Environment Features

### Using direnv for Auto-activation

```bash
# Install direnv
brew install direnv  # macOS
# sudo apt install direnv  # Ubuntu

# Create .envrc file
echo "source venv/bin/activate" > .envrc
direnv allow

# Now venv activates automatically when entering directory
```

### Virtual Environment with Specific Python Version

```bash
# With pyenv (Python version manager)
pyenv install 3.11.7
pyenv local 3.11.7
python -m venv venv

# Verify Python version in venv
source venv/bin/activate
python --version
```

### Environment Variables Management

```bash
# Create venv/bin/postactivate (runs after activation)
cat > venv/bin/postactivate << 'EOF'
export ENVIRONMENT=development
export DEBUG=true
export PYTHONPATH=$VIRTUAL_ENV:$PYTHONPATH
echo "🚀 FC Trading development environment activated"
EOF

chmod +x venv/bin/postactivate
```

## 🎯 Quick Reference Commands

```bash
# Essential Commands
python3 -m venv venv              # Create venv
source venv/bin/activate          # Activate (macOS/Linux)
venv\Scripts\activate             # Activate (Windows)
deactivate                        # Deactivate
pip install -r requirements.txt   # Install dependencies
pip freeze > requirements.txt     # Save current packages

# Management Commands
pip list                          # List installed packages
pip show package_name             # Package details
pip install --upgrade package     # Upgrade package
which python                      # Check Python path
echo $VIRTUAL_ENV                 # Check if venv active

# FC Trading Specific
./start.sh dev                    # Start development
./start.sh test                   # Run tests
cp .env.production .env           # Setup config
```

Với hướng dẫn này, bạn có thể dễ dàng tạo và quản lý virtual environment cho FC Trading API một cách chuyên nghiệp! 🐍✨
