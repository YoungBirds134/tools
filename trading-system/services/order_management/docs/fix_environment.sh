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
