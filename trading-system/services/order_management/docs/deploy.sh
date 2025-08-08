#!/bin/bash

# Production deployment script for FC Trading API with Telegram Bot

echo "🚀 Deploying FC Trading API with Telegram Bot..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

# Configuration
PROJECT_DIR="/opt/fc-trading"
SERVICE_USER="fctrading"
NGINX_CONFIG="/etc/nginx/sites-available/fc-trading"
SYSTEMD_SERVICE="/etc/systemd/system/fc-trading.service"
REDIS_SERVICE="redis-server"

# Create service user
echo "📋 Creating service user..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --shell /bin/bash --home-dir $PROJECT_DIR $SERVICE_USER
fi

# Create project directory
echo "📁 Setting up project directory..."
mkdir -p $PROJECT_DIR
chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# Copy application files
echo "📦 Copying application files..."
cp -r . $PROJECT_DIR/
chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update
apt-get install -y python3.11 python3.11-venv python3-pip nginx redis-server supervisor

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
sudo -u $SERVICE_USER python3.11 -m venv $PROJECT_DIR/venv
sudo -u $SERVICE_USER $PROJECT_DIR/venv/bin/pip install --upgrade pip
sudo -u $SERVICE_USER $PROJECT_DIR/venv/bin/pip install -r $PROJECT_DIR/requirements.txt

# Setup environment file
echo "⚙️ Setting up environment..."
if [ ! -f "$PROJECT_DIR/.env" ]; then
    cp $PROJECT_DIR/.env.example $PROJECT_DIR/.env
    echo "⚠️ Please edit $PROJECT_DIR/.env with your configuration"
fi
chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/.env

# Start Redis
echo "🗄️ Starting Redis..."
systemctl start redis-server
systemctl enable redis-server

# Create systemd service
echo "🔧 Creating systemd service..."
cat > $SYSTEMD_SERVICE << EOL
[Unit]
Description=FC Trading API with Telegram Bot
After=network.target redis.service
Requires=redis.service

[Service]
Type=exec
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/gunicorn app.main:app -c gunicorn.conf.py
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=10
KillMode=mixed
TimeoutStopSec=5

[Install]
WantedBy=multi-user.target
EOL

# Create Celery worker service
echo "🔧 Creating Celery worker service..."
cat > /etc/systemd/system/fc-trading-worker.service << EOL
[Unit]
Description=FC Trading Celery Worker
After=network.target redis.service
Requires=redis.service

[Service]
Type=exec
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/celery -A app.telegram.tasks.celery_app worker --loglevel=info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Create Celery beat service
echo "🔧 Creating Celery beat service..."
cat > /etc/systemd/system/fc-trading-beat.service << EOL
[Unit]
Description=FC Trading Celery Beat
After=network.target redis.service
Requires=redis.service

[Service]
Type=exec
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$PROJECT_DIR
Environment=PATH=$PROJECT_DIR/venv/bin
ExecStart=$PROJECT_DIR/venv/bin/celery -A app.telegram.tasks.celery_app beat --loglevel=info
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOL

# Setup Nginx configuration
echo "🌐 Setting up Nginx..."
cat > $NGINX_CONFIG << EOL
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Telegram webhook support
        proxy_read_timeout 60s;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
    }

    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
EOL

# Enable Nginx site
ln -sf $NGINX_CONFIG /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Create logs directory
echo "📝 Setting up logging..."
mkdir -p $PROJECT_DIR/logs
chown $SERVICE_USER:$SERVICE_USER $PROJECT_DIR/logs

# Setup log rotation
cat > /etc/logrotate.d/fc-trading << EOL
$PROJECT_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload fc-trading
    endscript
}
EOL

# Reload systemd and start services
echo "🔄 Starting services..."
systemctl daemon-reload

# Start and enable services
systemctl start fc-trading
systemctl enable fc-trading

systemctl start fc-trading-worker
systemctl enable fc-trading-worker

systemctl start fc-trading-beat
systemctl enable fc-trading-beat

systemctl restart nginx
systemctl enable nginx

# Setup firewall (if ufw is available)
if command -v ufw >/dev/null 2>&1; then
    echo "🔒 Configuring firewall..."
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
fi

# Display status
echo ""
echo "✅ Deployment completed!"
echo ""
echo "📊 Service Status:"
systemctl status fc-trading --no-pager -l
echo ""
systemctl status fc-trading-worker --no-pager -l
echo ""
systemctl status fc-trading-beat --no-pager -l
echo ""
systemctl status nginx --no-pager -l

echo ""
echo "🔧 Next Steps:"
echo "1. Edit $PROJECT_DIR/.env with your configuration"
echo "2. Restart services: systemctl restart fc-trading fc-trading-worker fc-trading-beat"
echo "3. Check logs: journalctl -f -u fc-trading"
echo "4. Test API: curl http://localhost/health"
echo "5. Setup SSL certificate (recommended: certbot)"
echo ""
echo "📱 Telegram Bot:"
echo "- Bot will start automatically if ENABLE_TELEGRAM_BOT=true"
echo "- Check webhook: curl http://localhost/api/v1/telegram/bot/info"
echo "- Send test message: curl -X POST http://localhost/api/v1/telegram/bot/send-message -H 'Content-Type: application/json' -d '{\"chat_id\":\"YOUR_CHAT_ID\",\"message\":\"Test message\"}'"
echo ""
echo "🎉 FC Trading API with Telegram Bot is now running!"
