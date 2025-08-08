-- Initialize FC Trading Database
-- This script creates the necessary tables and initial data

-- Create database if not exists (already handled by POSTGRES_DB env var)

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Create users table for persistent user data
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_user_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    fc_username VARCHAR(255),
    is_authenticated BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create sessions table for persistent session storage
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_user_id BIGINT NOT NULL,
    session_key VARCHAR(255) UNIQUE NOT NULL,
    session_data JSONB,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create trading_history table for trade logging
CREATE TABLE IF NOT EXISTS trading_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    order_id VARCHAR(255),
    symbol VARCHAR(50) NOT NULL,
    side VARCHAR(10) NOT NULL, -- BUY or SELL
    order_type VARCHAR(20) NOT NULL, -- LO, MP, ATO, ATC
    quantity INTEGER NOT NULL,
    price DECIMAL(15,3),
    status VARCHAR(20) DEFAULT 'PENDING',
    order_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    fill_time TIMESTAMP WITH TIME ZONE,
    fill_price DECIMAL(15,3),
    commission DECIMAL(15,3),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create notifications table for user notifications
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    message TEXT NOT NULL,
    notification_type VARCHAR(50) DEFAULT 'INFO', -- INFO, WARNING, ERROR, SUCCESS
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create watchlist table for user stock watchlists
CREATE TABLE IF NOT EXISTS watchlist (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    symbol VARCHAR(50) NOT NULL,
    added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, symbol)
);

-- Create market_data table for caching market data
CREATE TABLE IF NOT EXISTS market_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    symbol VARCHAR(50) NOT NULL,
    price DECIMAL(15,3),
    change_value DECIMAL(15,3),
    change_percent DECIMAL(8,4),
    volume BIGINT,
    high DECIMAL(15,3),
    low DECIMAL(15,3),
    open DECIMAL(15,3),
    close DECIMAL(15,3),
    market_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(symbol, market_time)
);

-- Create audit_logs table for system logging
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(100),
    entity_id VARCHAR(255),
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_telegram_user_id ON users(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_telegram_user_id ON user_sessions(telegram_user_id);
CREATE INDEX IF NOT EXISTS idx_user_sessions_session_key ON user_sessions(session_key);
CREATE INDEX IF NOT EXISTS idx_user_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX IF NOT EXISTS idx_trading_history_user_id ON trading_history(user_id);
CREATE INDEX IF NOT EXISTS idx_trading_history_symbol ON trading_history(symbol);
CREATE INDEX IF NOT EXISTS idx_trading_history_order_time ON trading_history(order_time);
CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_is_read ON notifications(is_read);
CREATE INDEX IF NOT EXISTS idx_watchlist_user_id ON watchlist(user_id);
CREATE INDEX IF NOT EXISTS idx_market_data_symbol ON market_data(symbol);
CREATE INDEX IF NOT EXISTS idx_market_data_market_time ON market_data(market_time);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_created_at ON audit_logs(created_at);

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at columns
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_sessions_updated_at BEFORE UPDATE ON user_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to clean expired sessions
CREATE OR REPLACE FUNCTION clean_expired_sessions()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM user_sessions WHERE expires_at < NOW();
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Create function to clean old audit logs (keep 90 days)
CREATE OR REPLACE FUNCTION clean_old_audit_logs()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM audit_logs WHERE created_at < NOW() - INTERVAL '90 days';
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Create function to clean old market data (keep 30 days)
CREATE OR REPLACE FUNCTION clean_old_market_data()
RETURNS INTEGER AS $$
DECLARE
    deleted_count INTEGER;
BEGIN
    DELETE FROM market_data WHERE created_at < NOW() - INTERVAL '30 days';
    GET DIAGNOSTICS deleted_count = ROW_COUNT;
    RETURN deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Grant permissions to application user
GRANT CONNECT ON DATABASE fc_trading TO fc_user;
GRANT USAGE ON SCHEMA public TO fc_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO fc_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO fc_user;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO fc_user;

-- Insert initial admin user (optional)
-- INSERT INTO users (telegram_user_id, username, first_name, is_authenticated)
-- VALUES (123456789, 'admin', 'System Admin', TRUE)
-- ON CONFLICT (telegram_user_id) DO NOTHING;

-- Log initialization
INSERT INTO audit_logs (action, entity_type, new_values, created_at)
VALUES ('SYSTEM_INIT', 'DATABASE', '{"version": "1.0", "initialized": true}', NOW());

-- Create view for user statistics
CREATE OR REPLACE VIEW user_stats AS
SELECT 
    u.id,
    u.telegram_user_id,
    u.username,
    u.created_at as user_created_at,
    COUNT(DISTINCT th.id) as total_trades,
    COUNT(DISTINCT w.id) as watchlist_count,
    COUNT(DISTINCT n.id) as total_notifications,
    COUNT(DISTINCT CASE WHEN n.is_read = FALSE THEN n.id END) as unread_notifications,
    MAX(u.last_login) as last_login
FROM users u
LEFT JOIN trading_history th ON u.id = th.user_id
LEFT JOIN watchlist w ON u.id = w.user_id
LEFT JOIN notifications n ON u.id = n.user_id
GROUP BY u.id, u.telegram_user_id, u.username, u.created_at;

-- Create view for daily trading summary
CREATE OR REPLACE VIEW daily_trading_summary AS
SELECT 
    DATE(order_time) as trading_date,
    COUNT(*) as total_orders,
    COUNT(CASE WHEN side = 'BUY' THEN 1 END) as buy_orders,
    COUNT(CASE WHEN side = 'SELL' THEN 1 END) as sell_orders,
    COUNT(CASE WHEN status = 'FILLED' THEN 1 END) as filled_orders,
    SUM(CASE WHEN status = 'FILLED' THEN quantity * COALESCE(fill_price, price) END) as total_value,
    SUM(CASE WHEN status = 'FILLED' THEN commission END) as total_commission
FROM trading_history
GROUP BY DATE(order_time)
ORDER BY trading_date DESC;

COMMIT;
