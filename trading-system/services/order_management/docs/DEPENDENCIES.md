# FC Trading API - Dependencies Documentation

## 📦 Core Dependencies Overview

### Framework và Web Server
- **FastAPI 0.104.1**: Modern web framework cho Python
- **Uvicorn 0.24.0**: ASGI server với high performance
- **Gunicorn 21.2.0**: Production WSGI server

### Data Validation và Configuration
- **Pydantic 2.5.0**: Data validation và serialization
- **Pydantic-settings 2.1.0**: Settings management từ environment

### Telegram Bot Integration
- **python-telegram-bot[all] 20.7**: Complete Telegram bot framework
- **cryptography 41.0.**: Security và encryption support

### Database và Caching
- **Redis 5.0.1**: In-memory data store cho caching và sessions
- **Celery 5.3.4**: Distributed task queue cho background jobs

### HTTP Client và API Integration
- **httpx 0.25.2**: Async HTTP client
- **ssi_fctrading**: SSI FastConnect Trading API client

### Development Tools
- **pytest 7.4.3**: Testing framework
- **pytest-asyncio 0.21.1**: Async testing support
- **pytest-cov 4.1.0**: Code coverage reports

### Code Quality
- **black 23.11.0**: Code formatter
- **isort 5.12.0**: Import sorter
- **flake8 6.1.0**: Linting tool
- **mypy 1.7.1**: Static type checker
- **pre-commit 3.6.0**: Git hooks framework

## 🔧 Installation Methods

### Method 1: Standard Installation
```bash
pip install -r requirements.txt
```

### Method 2: With Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Method 3: Development Installation
```bash
# Install with development dependencies
pip install -r requirements.txt
pip install -e .  # Editable install
```

## 📊 Dependency Categories

### Production Required (Always Install)
```
fastapi
uvicorn[standard]
pydantic
pydantic-settings
python-telegram-bot[all]
redis
celery
httpx
ssi_fctrading
gunicorn
cryptography
```

### Development Only (Optional)
```
pytest
pytest-asyncio
pytest-cov
black
isort
flake8
mypy
pre-commit
```

### Optional Production (Uncomment if needed)
```
psycopg2-binary     # PostgreSQL support
prometheus-client   # Metrics collection
```

## 🚀 Quick Install Commands

### Complete Setup
```bash
# All dependencies for full development
./setup_fc_trading.sh
```

### Minimal Production Setup
```bash
pip install fastapi uvicorn pydantic python-telegram-bot redis celery httpx ssi_fctrading gunicorn
```

### Testing Only
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Code Quality Only
```bash
pip install black isort flake8 mypy pre-commit
```

## 🔍 Dependency Verification

### Check Installation Status
```bash
# List all installed packages
pip list

# Check specific packages
pip show fastapi
pip show python-telegram-bot

# Verify imports
python -c "
import fastapi
import telegram
import redis
import celery
print('✅ All core dependencies working')
"
```

### Update Dependencies
```bash
# Check for outdated packages
pip list --outdated

# Update specific package
pip install --upgrade fastapi

# Update all packages (careful!)
pip install --upgrade -r requirements.txt
```

## 🐛 Common Issues và Solutions

### Issue: `ModuleNotFoundError: No module named 'xxx'`
```bash
# Solution: Install missing dependency
pip install package_name

# Or reinstall all requirements
pip install -r requirements.txt
```

### Issue: Package conflicts
```bash
# Solution: Clean install
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

### Issue: `telegram` import error
```bash
# Solution: Install with all extras
pip install "python-telegram-bot[all]"
```

### Issue: `redis` connection error
```bash
# Solution: Start Redis server
# macOS: brew services start redis
# Ubuntu: sudo systemctl start redis
# Docker: docker run -d -p 6379:6379 redis:alpine
```

### Issue: SSL/TLS errors với `ssi_fctrading`
```bash
# Solution: Update certificates
pip install --upgrade certifi
pip install --upgrade cryptography
```

## 📈 Performance Optimization

### Production Optimizations
```bash
# Install with no cache for smaller container
pip install --no-cache-dir -r requirements.txt

# Install only production deps
pip install --no-dev -r requirements.txt
```

### Memory Usage Optimization
```bash
# Install minimal versions
pip install fastapi uvicorn[standard] --no-deps
pip install pydantic --no-deps
```

## 🔒 Security Best Practices

### Pinned Versions
- All dependencies có exact versions để đảm bảo reproducible builds
- Regular security updates theo schedule

### Security Scanning
```bash
# Install security scanner
pip install safety

# Scan for vulnerabilities
safety check

# Check outdated packages với security issues
pip-audit
```

### Secure Installation
```bash
# Install with hash verification
pip install --require-hashes -r requirements.txt

# Install from trusted sources only
pip install --trusted-host pypi.org --trusted-host pypi.python.org
```

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Python Telegram Bot**: https://docs.python-telegram-bot.org/
- **Celery Documentation**: https://docs.celeryq.dev/
- **Redis Documentation**: https://redis.io/documentation
- **SSI FC Trading**: Check `docs/` directory
