# FC Trading API với Telegram Bot

Hệ thống trading API hoàn chỉnh với Telegram chatbot tích hợp cho SSI FastConnect Trading.

## 🚀 Tính Năng Chính

### 🤖 Telegram Chatbot
- **Xác thực an toàn**: OTP/PIN verification
- **Giao dịch thông minh**: Đặt/sửa/hủy lệnh qua chat
- **Theo dõi tài khoản**: Balance, position, lịch sử real-time
- **Giao diện trực quan**: Inline keyboards & menu navigation
- **Thông báo tức thì**: Alerts & notifications
- **Multi-session**: Quản lý nhiều user đồng thời

### 🔧 Production Features
- **High Performance**: Async/await, Redis caching
- **Scalable**: Celery background tasks, horizontal scaling
- **Secure**: Rate limiting, CORS, input validation
- **Monitoring**: Comprehensive logging, health checks
- **Deployment**: Docker, systemd, Nginx ready

## 📱 Telegram Bot Use Cases

### 1. Authentication Flow
```
/start → Main Menu → Authentication → Get OTP → Verify Code → Trading
```

### 2. Trading Operations
- **📈 New Orders**: Stock & Derivative markets
- **✏️ Modify Orders**: Price/quantity adjustments  
- **❌ Cancel Orders**: Quick order cancellation
- **📋 Order History**: Complete trading history
- **📖 Order Book**: Real-time order status

### 3. Account Management
- **💰 Balances**: Stock & Derivative accounts
- **📊 Positions**: Current holdings
- **⚡ PP/MMR**: Margin information
- **🔢 Max Quantities**: Available buying power

### 4. Smart Features
- **🔄 Auto-refresh**: Real-time data updates
- **📊 Pagination**: Large data sets handling
- **🎯 Quick Actions**: One-tap common operations
- **⚠️ Error Handling**: User-friendly error messages

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Telegram Bot  │    │   FastAPI App   │    │  FC Trading API │
│                 │    │                 │    │                 │
│  • Commands     │◄──►│  • REST API     │◄──►│  • Orders       │
│  • Keyboards    │    │  • Webhooks     │    │  • Accounts     │
│  • Sessions     │    │  • Auth         │    │  • Balances     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Redis       │    │     Celery      │    │    Logging      │
│  • Sessions     │    │  • Background   │    │  • Monitoring   │
│  • Cache        │    │  • Notifications│    │  • Errors       │
│  • Rate Limit   │    │  • Alerts       │    │  • Audit        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔧 Quick Setup

### 1. Environment Setup
```bash
# Clone project
cd fc-trading.py

# Setup environment
./setup.sh

# Configure Telegram Bot
cp .env.example .env
# Edit .env with your Telegram bot token
```

### 2. Development Mode
```bash
# Start Redis
redis-server

# Start API
python run.py

# Start Celery Worker (separate terminal)
celery -A app.telegram.tasks.celery_app worker --loglevel=info

# Start Celery Beat (separate terminal)  
celery -A app.telegram.tasks.celery_app beat --loglevel=info
```

### 3. Production Deployment
```bash
# Automated deployment
sudo ./deploy.sh

# Manual deployment with Docker
docker-compose up -d
```

## 📱 Telegram Bot Setup

### 1. Create Bot
```bash
# Talk to @BotFather on Telegram
/newbot
# Follow instructions to get bot token
```

### 2. Configure Bot
```bash
# Add to .env file
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_CHAT_IDS=["your_chat_id"]
ENABLE_TELEGRAM_BOT=true
```

### 3. Set Webhook (Production)
```bash
# Setup webhook URL
curl -X POST http://localhost:8000/api/v1/telegram/bot/webhook/setup

# Or use polling mode (Development)
ENABLE_WEBHOOK_MODE=false
```

## 🎯 API Endpoints

### Telegram Bot Management
```http
GET    /api/v1/telegram/bot/info           # Bot information
POST   /api/v1/telegram/bot/start          # Start bot
POST   /api/v1/telegram/bot/stop           # Stop bot
POST   /api/v1/telegram/webhook            # Webhook handler
GET    /api/v1/telegram/bot/stats          # Bot statistics
POST   /api/v1/telegram/bot/send-message   # Send message
POST   /api/v1/telegram/bot/broadcast      # Broadcast message
POST   /api/v1/telegram/bot/notification   # Send notification
```

### Trading Operations
```http
GET    /api/v1/auth/otp                    # Get OTP
POST   /api/v1/auth/verify-code            # Verify code
POST   /api/v1/orders/new-order            # Place order
PUT    /api/v1/orders/modify-order         # Modify order
DELETE /api/v1/orders/cancel-order         # Cancel order
GET    /api/v1/accounts/stock/balance      # Get balance
```

## 🎮 Bot Commands

### Basic Commands
- `/start` - Khởi động bot
- `/help` - Hướng dẫn sử dụng  
- `/menu` - Menu chính
- `/status` - Trạng thái tài khoản
- `/logout` - Đăng xuất

### Interactive Menus
- **🔐 Authentication** - Xác thực tài khoản
- **📊 Orders** - Quản lý lệnh giao dịch
- **💼 Account Info** - Thông tin tài khoản  
- **❓ Help** - Trợ giúp

## 💡 Usage Examples

### 1. Authentication
```
User: /start
Bot: Welcome! Please authenticate first.
User: [Clicks "Get OTP"]
Bot: OTP sent to your phone. Click "Verify Code"
User: [Clicks "Verify Code"]
Bot: Enter verification code:
User: 123456
Bot: ✅ Authentication successful!
```

### 2. Place Order
```
User: [Clicks "New Stock Order"]
Bot: Select market: VN or VNFE
User: [Clicks "VN"]
Bot: Select Buy or Sell
User: [Clicks "Buy"]
Bot: Select order type
User: [Clicks "Limit Order"]
Bot: Send: Symbol,Price,Quantity,Account
User: VCB,95000,100,123456
Bot: Confirm order? ✅ Confirm ❌ Cancel
User: [Clicks "Confirm"]
Bot: ✅ Order placed successfully!
```

### 3. Check Balance
```
User: [Clicks "Account Info" → "Stock Balance"]
Bot: 💰 Stock Balance
     Available: 10,000,000 VND
     Total Assets: 50,000,000 VND
     Buying Power: 8,000,000 VND
```

## 🔒 Security Features

### Bot Security
- **Chat ID Whitelist**: Restrict access to authorized users
- **Session Management**: Secure user sessions with Redis
- **Rate Limiting**: Prevent spam and abuse
- **Input Validation**: Sanitize all user inputs
- **Error Handling**: No sensitive data in error messages

### API Security  
- **Authentication Required**: All trading operations need auth
- **CORS Protection**: Cross-origin request filtering
- **Request Logging**: Comprehensive audit trail
- **Environment Secrets**: No hardcoded credentials

## 📊 Monitoring & Analytics

### Bot Analytics
```http
GET /api/v1/telegram/bot/stats
{
  "active_users": 25,
  "bot_running": true,
  "bot_username": "fc_trading_bot",
  "webhook_enabled": true
}
```

### Health Monitoring
```http
GET /health
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-07-16T10:30:00Z"
}
```

### Logging
- **Application Logs**: `logs/app.log`
- **Access Logs**: `logs/access.log` 
- **Error Logs**: `logs/error.log`
- **Bot Logs**: Included in application logs

## 🚀 Production Checklist

### ✅ Environment
- [x] Environment variables configured
- [x] Redis server running
- [x] SSL certificate (optional)
- [x] Domain name configured
- [x] Firewall rules

### ✅ Bot Configuration
- [x] Telegram bot token
- [x] Webhook URL set
- [x] Admin chat IDs configured
- [x] Rate limiting enabled
- [x] Error handling tested

### ✅ Services
- [x] FastAPI application
- [x] Celery worker
- [x] Celery beat scheduler
- [x] Redis server
- [x] Nginx reverse proxy

### ✅ Monitoring
- [x] Health checks
- [x] Log rotation
- [x] Service monitoring
- [x] Bot analytics
- [x] Error notifications

## 🔧 Troubleshooting

### Bot Not Responding
```bash
# Check bot status
curl http://localhost:8000/api/v1/telegram/bot/info

# Check logs
journalctl -f -u fc-trading

# Restart bot
curl -X POST http://localhost:8000/api/v1/telegram/bot/stop
curl -X POST http://localhost:8000/api/v1/telegram/bot/start
```

### Webhook Issues
```bash
# Delete webhook
curl -X DELETE http://localhost:8000/api/v1/telegram/bot/webhook

# Setup new webhook
curl -X POST http://localhost:8000/api/v1/telegram/bot/webhook/setup
```

### Session Problems
```bash
# Check Redis connection
redis-cli ping

# Clear user session
redis-cli del "telegram_user:USER_ID"
```

## 📝 Development

### Adding New Commands
```python
# 1. Add handler in handlers.py
@staticmethod
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Command logic here
    pass

# 2. Register in bot.py
self.application.add_handler(CommandHandler("newcmd", TelegramHandlers.new_command))
```

### Adding New Keyboards
```python
# Add to keyboards.py
@staticmethod
def new_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="option1")],
        [InlineKeyboardButton("Option 2", callback_data="option2")]
    ]
    return InlineKeyboardMarkup(keyboard)
```

### Background Tasks
```python
# Add to tasks.py
@celery_app.task(bind=True)
def new_background_task(self, data):
    # Task logic here
    return {"success": True}
```

## 🆘 Support

### Documentation
- **FastAPI Docs**: http://localhost:8000/docs
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Python Telegram Bot**: https://python-telegram-bot.org/

### Common Issues
- **Bot Token Invalid**: Check token format and permissions
- **Redis Connection**: Ensure Redis is running and accessible
- **Webhook SSL**: HTTPS required for production webhooks
- **Rate Limiting**: Adjust limits in configuration

### Contact
- **Email**: support@example.com
- **Issues**: GitHub Issues
- **Documentation**: Project README

---

🎉 **FC Trading API với Telegram Bot** - Professional trading automation solution!

Hệ thống hoàn chỉnh để giao dịch chứng khoán qua Telegram với tất cả tính năng production-ready!
