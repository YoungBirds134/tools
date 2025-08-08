# Python Version Management Guide

## 🐍 Supported Python Versions

FC Trading API supports Python 3.9+ with the following recommendations:

- **Python 3.11+**: ✅ **Recommended** - Best performance and latest features
- **Python 3.10**: ✅ **Good** - Stable and well-supported  
- **Python 3.9**: ⚠️ **Supported** - Minimum version, but older

## 🔧 Managing Python Versions

### Check Available Python Versions

```bash
# Check all available Python versions
./check_python.sh

# Manual check
python3.11 --version  # Try specific versions
python3.10 --version
python3.9 --version
python3 --version      # Default python3
```

### Install Multiple Python Versions

#### macOS (using Homebrew):
```bash
# Install multiple Python versions
brew install python@3.11
brew install python@3.10  
brew install python@3.9

# Check installations
ls -la /opt/homebrew/bin/python3*
```

#### Ubuntu/Debian:
```bash
# Add deadsnakes PPA for multiple Python versions
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update

# Install specific versions
sudo apt install python3.11 python3.11-pip python3.11-venv
sudo apt install python3.10 python3.10-pip python3.10-venv
sudo apt install python3.9 python3.9-pip python3.9-venv
```

#### Using pyenv (recommended for developers):
```bash
# Install pyenv
curl https://pyenv.run | bash

# Install multiple Python versions
pyenv install 3.11.7
pyenv install 3.10.13
pyenv install 3.9.18

# Set global default
pyenv global 3.11.7

# Set local version for project
cd fc-trading.py
pyenv local 3.10.13
```

## 🛠️ Virtual Environment Scenarios

### Scenario 1: Virtual Environment Already Exists

When you run `./setup_fc_trading.sh` and venv already exists:

```bash
🔄 Virtual environment already exists
Options:
  1. Use existing virtual environment (recommended)
  2. Recreate virtual environment (will reinstall all packages)  
  3. Exit and handle manually

Choose option (1/2/3): 
```

**Recommendations:**
- Choose **1** if your current venv works fine
- Choose **2** if you want to change Python version or fix issues
- Choose **3** if you want manual control

### Scenario 2: Python Version Mismatch

If existing venv has different Python version:

```bash
⚠️ Virtual environment Python (3.11.5) differs from current Python (3.9.18)
Options:
  1. Recreate virtual environment (recommended)
  2. Try to use existing anyway
  3. Exit and handle manually
```

**Recommendation:** Choose **1** to avoid compatibility issues

### Scenario 3: Want to Use Specific Python Version

```bash
# Method 1: Use fix_environment.sh
./fix_environment.sh

# Method 2: Manual recreation
rm -rf venv
python3.9 -m venv venv  # Use specific Python version
source venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Quick Setup Commands

### For Python 3.9 Users

```bash
# Option 1: Automated setup (will detect Python 3.9)
./setup_fc_trading.sh

# Option 2: Manual setup with Python 3.9
rm -rf venv
python3.9 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.production .env
```

### For Multiple Python Environments

```bash
# Create environments for different Python versions
python3.11 -m venv venv-py311
python3.10 -m venv venv-py310  
python3.9 -m venv venv-py39

# Use specific environment
source venv-py39/bin/activate
pip install -r requirements.txt
```

## 🔧 Troubleshooting Tools

### 1. Check Python Status
```bash
./check_python.sh
```
Shows:
- Available Python versions
- Current virtual environment status
- Activation status
- Recommendations

### 2. Fix Environment Issues
```bash
./fix_environment.sh
```
Options:
- Recreate with Python 3.11
- Recreate with Python 3.10
- Recreate with Python 3.9
- Auto-detect best version

### 3. Verify Complete Setup
```bash
./check_setup.sh
```
Checks:
- Python paths
- Package installations
- Configuration files
- Project structure

## ⚠️ Common Issues and Solutions

### Issue 1: `python3.9: command not found`

**Solutions:**
```bash
# macOS
brew install python@3.9

# Ubuntu
sudo apt install python3.9 python3.9-pip python3.9-venv

# Check installation
which python3.9
python3.9 --version
```

### Issue 2: Virtual Environment Won't Activate

**Solutions:**
```bash
# Check if venv exists and is valid
./check_python.sh

# Recreate if corrupted
./fix_environment.sh

# Manual fix
rm -rf venv
python3.9 -m venv venv
source venv/bin/activate
```

### Issue 3: Package Installation Fails

**Solutions:**
```bash
# Update pip first
pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Check for specific Python version requirements
python -c "import sys; print(sys.version_info)"
```

### Issue 4: Import Errors After Setup

**Solutions:**
```bash
# Verify installation
./check_setup.sh

# Check Python path
which python
echo $VIRTUAL_ENV

# Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

## 🎯 Best Practices

### 1. Version Consistency
- Use same Python version across development, testing, and production
- Document Python version requirements in README
- Use version-specific requirements if needed

### 2. Environment Isolation
```bash
# Always use virtual environments
python3.9 -m venv venv
source venv/bin/activate

# Never install packages globally
pip install package  # ✅ Good (in venv)
sudo pip install package  # ❌ Bad (global)
```

### 3. Requirements Management
```bash
# Pin exact versions for production
pip freeze > requirements-exact.txt

# Use loose versions for development  
pip install package>=1.0,<2.0
```

### 4. Multiple Environment Testing
```bash
# Test with different Python versions
for py in python3.9 python3.10 python3.11; do
    echo "Testing with $py"
    $py -m venv test-venv
    source test-venv/bin/activate
    pip install -r requirements.txt
    python -m pytest
    deactivate
    rm -rf test-venv
done
```

## 📊 Performance Comparison

| Python Version | Speed | Features | Recommendation |
|---------------|--------|----------|----------------|
| 3.11.x | ⚡⚡⚡ Fastest | Latest features | ✅ Best choice |
| 3.10.x | ⚡⚡ Fast | Pattern matching | ✅ Good choice |
| 3.9.x | ⚡ Standard | Stable | ⚠️ Minimum |

## 🔗 Quick Reference

```bash
# Essential Commands
./setup_fc_trading.sh     # Complete setup
./check_python.sh         # Check Python status  
./fix_environment.sh      # Fix environment issues
source venv/bin/activate   # Activate venv
deactivate                # Deactivate venv

# Python Version Commands  
python3.9 -m venv venv    # Create with Python 3.9
python3.10 -m venv venv   # Create with Python 3.10
python3.11 -m venv venv   # Create with Python 3.11

# Verification Commands
python --version          # Check active Python
which python             # Check Python path
pip list                 # List installed packages
```

Với hệ thống này, bạn có thể dễ dàng quản lý Python 3.9 và các virtual environments khác nhau! 🐍✨
