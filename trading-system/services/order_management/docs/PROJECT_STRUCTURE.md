# FC Trading API - File Structure

This document explains the cleaned up project structure after removing unnecessary files.

## 📁 Project Structure

```
fc-trading.py/
├── 📄 README.md                    # Main documentation
├── 📄 requirements.txt             # Python dependencies
├── 📄 run.py                       # Application entry point
├── 📄 start.sh                     # Quick start script ⭐
├── 📄 .env.production               # Environment template
├── 📄 .env.example                 # Environment example
├── 📄 .gitignore                   # Git ignore rules
│
├── 🐳 Dockerfile                   # Container definition
├── 🐳 docker-compose.yml           # Main orchestration
├── 🐳 docker-compose.prod.yml      # Production orchestration
├── 🗄️ init.sql                     # Database initialization
├── ⚙️ redis.conf                   # Redis configuration
├── ⚙️ gunicorn.conf.py             # WSGI server config
├── 📋 pyproject.toml               # Python project config
│
├── 🚀 deploy.sh                    # Development deployment
├── 🚀 deploy-prod.sh               # Production deployment
├── 🛠️ setup-dev.sh                 # Development setup
│
├── 📚 DOCS.md                      # Additional documentation
├── 📚 DEPLOYMENT.md                # Deployment guide
├── 📚 TELEGRAM_BOT.md              # Bot documentation
├── 📚 CHANGELOG.md                 # Version history
│
├── 🏗️ app/                         # Main application
│   ├── __init__.py
│   ├── main.py                     # FastAPI app
│   ├── config.py                   # Settings
│   ├── models.py                   # Data models
│   ├── middleware.py               # Custom middleware
│   │
│   ├── 🔌 routers/                 # API endpoints
│   │   ├── __init__.py
│   │   ├── auth.py                 # Authentication
│   │   ├── accounts.py             # Account management
│   │   ├── orders.py               # Trading orders
│   │   └── telegram.py             # Telegram webhook
│   │
│   ├── 🤖 telegram/                # Telegram bot
│   │   ├── __init__.py
│   │   ├── bot.py                  # Bot instance
│   │   ├── handlers.py             # Message handlers
│   │   ├── keyboards.py            # UI keyboards
│   │   ├── session.py              # Session management
│   │   ├── manager.py              # Bot manager
│   │   └── tasks.py                # Background tasks
│   │
│   ├── 🔧 services/                # Business logic
│   │   ├── __init__.py
│   │   └── fc_service.py           # Trading service
│   │
│   └── 🛠️ utils/                   # Utilities
│       ├── __init__.py
│       ├── logging.py              # Logging config
│       └── helpers.py              # Helper functions
│
├── 🌐 nginx/                       # Reverse proxy
│   └── nginx.conf                  # Nginx configuration
│
├── 📊 monitoring/                  # Monitoring stack
│   └── prometheus.yml              # Metrics config
│
├── 📖 docs/                        # Documentation files
│   ├── HƯỚNG DẪN SỬ DỤNG FASTCONNECT TRADING.pdf
│   └── SSI_FastConnectTrading_Specs_v2.4.pdf
│
└── 🧪 tests/                       # Test suite
    ├── __init__.py
    └── test_main.py
```

## 🗑️ Removed Files

The following files were cleaned up to reduce clutter:

### Windows-specific files (not needed on macOS):
- ❌ `example_api.bat`
- ❌ `example_stream.bat` 
- ❌ `install_examples.bat`

### Duplicate/redundant files:
- ❌ `examples/` directory (old structure)
- ❌ `examples/requirements.txt` (duplicate)
- ❌ `nginx.conf` (moved to `nginx/nginx.conf`)
- ❌ `setup.sh` (replaced by `setup-dev.sh`)
- ❌ `dist/` directory (build artifacts)

### System files:
- ❌ `.DS_Store` (macOS system file)

## 📋 File Categories

### 🔧 Core Application
- `app/` - Main application code
- `requirements.txt` - Dependencies
- `run.py` - Entry point

### 🚀 Deployment & Scripts
- `start.sh` - ⭐ **NEW**: Universal start script
- `deploy.sh` - Development deployment
- `deploy-prod.sh` - Production deployment
- `setup-dev.sh` - Development setup

### 🐳 Containerization
- `Dockerfile` - Container definition
- `docker-compose.yml` - Development orchestration
- `docker-compose.prod.yml` - Production orchestration

### ⚙️ Configuration
- `.env.production` - Environment template
- `redis.conf` - Redis settings
- `gunicorn.conf.py` - WSGI settings
- `nginx/nginx.conf` - Proxy settings

### 📚 Documentation
- `README.md` - Main guide
- `TELEGRAM_BOT.md` - Bot documentation
- `DEPLOYMENT.md` - Deployment guide
- `DOCS.md` - Additional docs

## ⭐ New Features

### Universal Start Script (`start.sh`)
A new intelligent start script that handles different modes:

```bash
./start.sh dev      # Development mode
./start.sh prod     # Production mode  
./start.sh bot      # Bot only mode
./start.sh test     # Run tests
```

The script automatically:
- ✅ Checks dependencies
- ✅ Creates virtual environment
- ✅ Installs requirements
- ✅ Validates configuration
- ✅ Starts appropriate mode

## 🎯 Quick Commands Summary

```bash
# Super quick start
cp .env.production .env && ./start.sh dev

# Production deployment
./start.sh prod

# Bot development
./start.sh bot

# Run tests
./start.sh test
```

This cleaned up structure provides a professional, production-ready codebase with clear organization and easy deployment options.
