#!/bin/bash
# FC Trading API - Complete Environment Setup Script

set -e

echo "🚀 FC Trading API - Complete Environment Setup"
echo "=============================================="

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log() { echo -e "${GREEN}[INFO]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
info() { echo -e "${BLUE}[STEP]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# Step 1: Check Python installation and version
info "Checking Python installation and version..."

# Function echo "💡 Pro tip: To activate the environment quickly in the future:"
echo "   source activate.sh"
echo "   # or manually:"
echo "   source venv/bin/activate"
echo ""
echo "🔧 Troubleshooting tools:"
echo "   ./check_python.sh     - Check Python versions"
echo "   ./fix_environment.sh  - Fix environment issues"
echo "   ./check_setup.sh      - Verify complete setup"heck Python version
check_python_version() {
    local python_cmd=$1
    if command -v $python_cmd &> /dev/null; then
        local version=$($python_cmd --version 2>&1 | cut -d' ' -f2)
        local major=$(echo $version | cut -d'.' -f1)
        local minor=$(echo $version | cut -d'.' -f2)
        echo "$version $major $minor"
        return 0
    fi
    return 1
}

# Try different Python commands
PYTHON_CMD=""
PYTHON_VERSION=""
PYTHON_MAJOR=""
PYTHON_MINOR=""

for cmd in python3.11 python3.10 python3.9 python3 python; do
    if result=$(check_python_version $cmd); then
        read version major minor <<< "$result"
        if [[ $major -eq 3 && $minor -ge 9 ]]; then
            PYTHON_CMD=$cmd
            PYTHON_VERSION=$version
            PYTHON_MAJOR=$major
            PYTHON_MINOR=$minor
            break
        fi
    fi
done

if [[ -z "$PYTHON_CMD" ]]; then
    error "Python 3.9+ is required but not found. Please install Python 3.9+ first:
  macOS: brew install python@3.11 python@3.10 python@3.9
  Ubuntu: sudo apt install python3.11 python3.11-pip python3.11-venv
  Windows: Download from python.org"
fi

log "Using Python: $PYTHON_CMD (version $PYTHON_VERSION)"

# Version recommendations
if [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 11 ]]; then
    log "✅ Excellent! Python 3.11+ provides best performance"
elif [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -eq 10 ]]; then
    log "✅ Good! Python 3.10 is well supported"
elif [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -eq 9 ]]; then
    warn "Python 3.9 is supported but 3.10+ is recommended for better performance"
else
    warn "Python $PYTHON_VERSION detected. Consider upgrading to 3.10+ for optimal experience"
fi

# Step 2: Handle Virtual Environment
info "Checking virtual environment..."

# Function to check if venv is valid
check_venv_validity() {
    if [[ -d "venv" ]]; then
        # Check if venv has correct Python version
        if [[ -f "venv/bin/python" ]]; then
            local venv_version=$(venv/bin/python --version 2>&1 | cut -d' ' -f2)
            local venv_major=$(echo $venv_version | cut -d'.' -f1)
            local venv_minor=$(echo $venv_version | cut -d'.' -f2)
            
            log "Existing venv Python version: $venv_version"
            
            # Check if venv Python matches current Python
            if [[ "$venv_major.$venv_minor" == "$PYTHON_MAJOR.$PYTHON_MINOR" ]]; then
                log "✅ Virtual environment Python version matches current Python"
                return 0
            else
                warn "⚠️  Virtual environment Python ($venv_version) differs from current Python ($PYTHON_VERSION)"
                return 1
            fi
        else
            warn "Virtual environment appears corrupted (missing python executable)"
            return 1
        fi
    fi
    return 2  # venv doesn't exist
}

# Function to create virtual environment
create_venv() {
    info "Creating virtual environment with $PYTHON_CMD..."
    if $PYTHON_CMD -m venv venv; then
        if [[ -f "venv/bin/activate" ]]; then
            log "✅ Virtual environment created successfully"
            return 0
        else
            error "Virtual environment created but activation script missing"
            return 1
        fi
    else
        error "Failed to create virtual environment"
        return 1
    fi
}

# Check venv status
set +e  # Temporarily disable exit on error
check_venv_validity
venv_status=$?
set -e  # Re-enable exit on error
NEED_TO_CREATE_VENV=false
VENV_READY=false

case $venv_status in
    0)  # Valid venv exists
        log "Valid virtual environment found"
        echo ""
        echo "Options:"
        echo "  1. Use existing virtual environment (recommended)"
        echo "  2. Recreate virtual environment (will reinstall all packages)"
        echo "  3. Exit and handle manually"
        echo ""
        read -p "Choose option (1/2/3) [default: 1]: " choice
        choice=${choice:-1}
        
        case $choice in
            1)
                log "Using existing virtual environment"
                VENV_READY=true
                ;;
            2)
                warn "Recreating virtual environment..."
                rm -rf venv
                if create_venv; then
                    VENV_READY=true
                fi
                ;;
            3)
                info "Exiting. You can manually manage your virtual environment:"
                echo "  Remove: rm -rf venv"
                echo "  Create: $PYTHON_CMD -m venv venv"
                exit 0
                ;;
            *)
                warn "Invalid choice. Using existing virtual environment"
                VENV_READY=true
                ;;
        esac
        ;;
    1)  # Invalid venv exists
        warn "Virtual environment exists but has issues"
        echo ""
        echo "Issues detected:"
        echo "  - Python version mismatch, or"
        echo "  - Corrupted virtual environment"
        echo ""
        echo "Options:"
        echo "  1. Recreate virtual environment (recommended)"
        echo "  2. Try to use existing anyway"
        echo "  3. Exit and handle manually"
        echo ""
        read -p "Choose option (1/2/3) [default: 1]: " choice
        choice=${choice:-1}
        
        case $choice in
            1)
                warn "Recreating virtual environment..."
                rm -rf venv
                if create_venv; then
                    VENV_READY=true
                fi
                ;;
            2)
                warn "Attempting to use existing virtual environment"
                if [[ -f "venv/bin/activate" ]]; then
                    VENV_READY=true
                else
                    error "Cannot use existing venv - activation script missing"
                fi
                ;;
            3)
                info "Exiting. Please handle virtual environment manually"
                exit 0
                ;;
            *)
                warn "Invalid choice. Recreating virtual environment..."
                rm -rf venv
                if create_venv; then
                    VENV_READY=true
                fi
                ;;
        esac
        ;;
    2)  # No venv exists
        if create_venv; then
            VENV_READY=true
        fi
        ;;
esac

# Step 3: Activate Virtual Environment
if [[ "$VENV_READY" == "true" ]]; then
    info "Activating virtual environment..."
    if [[ -f "venv/bin/activate" ]]; then
        source venv/bin/activate
        
        # Verify activation
        if [[ "$VIRTUAL_ENV" != "" ]]; then
            log "✅ Virtual environment activated: $VIRTUAL_ENV"
        else
            error "Failed to activate virtual environment"
        fi
    else
        error "Virtual environment activation script not found"
    fi
else
    error "Virtual environment is not ready. Cannot continue."
fi

# Step 4: Upgrade pip
info "Upgrading pip to latest version..."
pip install --upgrade pip
pip_version=$(pip --version | cut -d' ' -f2)
log "pip upgraded to version: $pip_version"

# Step 5: Install Requirements
info "Installing FC Trading dependencies..."
if [ -f "requirements.txt" ]; then
    log "Installing packages from requirements.txt..."
    pip install -r requirements.txt
    log "Dependencies installed successfully"
    
    # Show installed packages
    echo ""
    log "Installed packages summary:"
    pip list | head -10
    total_packages=$(pip list | wc -l)
    log "Total packages installed: $((total_packages - 2))"
else
    warn "requirements.txt not found, skipping package installation"
fi

# Step 6: Setup Environment Configuration
info "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.production" ]; then
        cp .env.production .env
        log "Environment file created from template"
        warn "⚠️  IMPORTANT: Please update .env with your actual credentials!"
        echo ""
        echo "Required credentials to update in .env:"
        echo "  - TELEGRAM_BOT_TOKEN (from @BotFather)"
        echo "  - FC_USERNAME (your FastConnect username)"
        echo "  - FC_PASSWORD (your FastConnect password)"
        echo "  - FC_PIN (your FastConnect PIN)"
        echo "  - SECRET_KEY (generate a secure random key)"
    else
        warn ".env.production template not found"
        echo "Creating basic .env file..."
        cat > .env << 'EOF'
# FC Trading API Configuration
ENVIRONMENT=development
DEBUG=true
TELEGRAM_BOT_TOKEN=your-bot-token-here
FC_USERNAME=your-username
FC_PASSWORD=your-password
FC_PIN=your-pin
SECRET_KEY=change-this-secret-key
REDIS_URL=redis://localhost:6379/0
EOF
        log "Basic .env file created"
    fi
else
    log "Environment file already exists"
fi

# Step 7: Enhanced Verification
info "Verifying installation and compatibility..."

# Check Python version in venv
venv_python_version=$(python --version 2>&1 | cut -d' ' -f2)
log "Virtual environment Python version: $venv_python_version"

# Comprehensive dependency check
python -c "
import sys
print('✅ Python executable:', sys.executable)
print('✅ Python version:', sys.version.split()[0])
print('✅ Python path:', sys.path[0] if sys.path else 'Not set')

# Check required packages
required_packages = {
    'fastapi': 'FastAPI framework',
    'uvicorn': 'ASGI server',
    'pydantic': 'Data validation',
    'telegram': 'Telegram bot library',
    'redis': 'Redis client',
    'celery': 'Task queue',
    'httpx': 'HTTP client',
    'cryptography': 'Cryptographic library'
}

missing_packages = []
for package, description in required_packages.items():
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        print(f'✅ {package}: {version} ({description})')
    except ImportError:
        print(f'❌ {package}: not installed ({description})')
        missing_packages.append(package)

# Check optional packages
optional_packages = {
    'pytest': 'Testing framework',
    'black': 'Code formatter',
    'mypy': 'Type checker'
}

for package, description in optional_packages.items():
    try:
        module = __import__(package)
        version = getattr(module, '__version__', 'unknown')
        print(f'📦 {package}: {version} ({description})')
    except ImportError:
        print(f'📦 {package}: not installed ({description}) - optional')

if missing_packages:
    missing_str = ', '.join(missing_packages)
    print(f'\\n⚠️  Missing required packages: {missing_str}')
    print('Try running: pip install -r requirements.txt')
    sys.exit(1)
else:
    print('\\n✅ All required dependencies are installed and working!')

# Check SSI FCTrading specifically
try:
    import ssi_fctrading
    print('✅ SSI FCTrading library available')
except ImportError:
    print('⚠️  SSI FCTrading library not found - this may be expected in some environments')
"

# Step 8: Create helpful scripts
info "Creating helper scripts..."

# Create activate script
cat > activate.sh << 'EOF'
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
EOF

chmod +x activate.sh

# Create check script
cat > check_setup.sh << 'EOF'
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
EOF

chmod +x check_setup.sh

# Additional helper: Python version checker
cat > check_python.sh << 'EOF'
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
EOF

chmod +x check_python.sh

# Additional helper: Environment fixer
cat > fix_environment.sh << 'EOF'
#!/bin/bash
# Environment Fixer for FC Trading API

echo "🔧 FC Trading Environment Fixer"
echo "==============================="
echo ""

# Function to recreate venv with specific Python version
recreate_venv() {
    local python_cmd=$1
    echo "🔄 Recreating virtual environment with $python_cmd..."
    
    if [[ -d "venv" ]]; then
        echo "📁 Removing existing venv..."
        rm -rf venv
    fi
    
    if $python_cmd -m venv venv; then
        echo "✅ Virtual environment created successfully"
        source venv/bin/activate
        pip install --upgrade pip
        
        if [[ -f "requirements.txt" ]]; then
            echo "📦 Installing requirements..."
            pip install -r requirements.txt
            echo "✅ Requirements installed"
        fi
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
}

echo "Available options:"
echo "1. Recreate venv with Python 3.11 (recommended)"
echo "2. Recreate venv with Python 3.10"
echo "3. Recreate venv with Python 3.9"
echo "4. Auto-detect best Python version"
echo "5. Exit"
echo ""

read -p "Choose option (1-5): " choice

case $choice in
    1)
        if command -v python3.11 &> /dev/null; then
            recreate_venv python3.11
        else
            echo "❌ Python 3.11 not found"
            exit 1
        fi
        ;;
    2)
        if command -v python3.10 &> /dev/null; then
            recreate_venv python3.10
        else
            echo "❌ Python 3.10 not found"
            exit 1
        fi
        ;;
    3)
        if command -v python3.9 &> /dev/null; then
            recreate_venv python3.9
        else
            echo "❌ Python 3.9 not found"
            exit 1
        fi
        ;;
    4)
        for cmd in python3.11 python3.10 python3.9 python3; do
            if command -v $cmd &> /dev/null; then
                recreate_venv $cmd
                break
            fi
        done
        ;;
    5)
        echo "👋 Exiting..."
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Environment fixed successfully!"
echo "🚀 You can now run: ./start.sh dev"
EOF

chmod +x fix_environment.sh

log "Helper scripts created: activate.sh, check_setup.sh"
log "Additional helper scripts created: check_python.sh, fix_environment.sh"

# Step 9: Test basic import
info "Testing basic application import..."
if python -c "from app.main import app; print('✅ Application imports successfully')" 2>/dev/null; then
    log "Application structure verified"
else
    warn "Application import test failed - this is normal if dependencies are missing"
fi

# Step 10: Final summary
echo ""
log "🎉 Setup completed successfully!"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Next Steps:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 🔑 Update credentials in .env:"
echo "   nano .env"
echo ""
echo "2. 🚀 Start the application:"
echo "   ./start.sh dev"
echo ""
echo "3. 🤖 Or start only the Telegram bot:"
echo "   ./start.sh bot"
echo ""
echo "4. 🧪 Run tests:"
echo "   ./start.sh test"
echo ""
echo "5. 🔍 Verify setup anytime:"
echo "   ./check_setup.sh"
echo ""
echo "6. 🐍 Check Python versions:"
echo "   ./check_python.sh"
echo ""
echo "7. 🔧 Fix environment issues:"
echo "   ./fix_environment.sh"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📚 Documentation:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "• Virtual Environment Guide: VIRTUAL_ENVIRONMENT_GUIDE.md"
echo "• Telegram Bot Guide: TELEGRAM_BOT.md"
echo "• Deployment Guide: DEPLOYMENT.md"
echo "• API Docs: http://localhost:8000/docs (after starting)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Step 11: Auto-activation tip
echo ""
info "💡 Pro tip: To activate the environment quickly in the future:"
echo "   source activate.sh"
echo "   # or manually:"
echo "   source venv/bin/activate"
