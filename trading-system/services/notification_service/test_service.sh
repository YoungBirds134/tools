#!/bin/bash

# Test script for Trading Notification Service
# Comprehensive testing of all endpoints and functionality

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
BASE_URL="http://localhost:8001"
TEST_USER_ID="123456789"

print_test() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
}

print_info() {
    echo -e "${YELLOW}[INFO]${NC} $1"
}

# Function to make HTTP requests and check status
test_endpoint() {
    local method=$1
    local endpoint=$2
    local expected_status=${3:-200}
    local data=$4
    local description=$5
    
    print_test "$description"
    
    if [ -n "$data" ]; then
        response=$(curl -s -w "%{http_code}" -X "$method" \
            -H "Content-Type: application/json" \
            -d "$data" \
            "$BASE_URL$endpoint")
    else
        response=$(curl -s -w "%{http_code}" -X "$method" "$BASE_URL$endpoint")
    fi
    
    status_code="${response: -3}"
    body="${response%???}"
    
    if [ "$status_code" -eq "$expected_status" ]; then
        print_success "Status: $status_code (Expected: $expected_status)"
        if [ -n "$body" ] && [ "$body" != "null" ]; then
            echo "$body" | python -m json.tool 2>/dev/null || echo "$body"
        fi
        echo ""
        return 0
    else
        print_fail "Status: $status_code (Expected: $expected_status)"
        echo "Response: $body"
        echo ""
        return 1
    fi
}

echo "🧪 Testing Trading Notification Service"
echo "========================================"
echo ""

# Test 1: Root endpoint
test_endpoint "GET" "/" 200 "" "Testing root endpoint"

# Test 2: Health check
test_endpoint "GET" "/api/v1/health/" 200 "" "Testing health check"

# Test 3: Liveness probe
test_endpoint "GET" "/api/v1/health/live" 200 "" "Testing liveness probe"

# Test 4: Send test notification
test_data='{
  "user_id": "'$TEST_USER_ID'",
  "notification_type": "system_maintenance",
  "title": "Test Notification",
  "message": "This is a test notification from the automated test suite",
  "priority": "low"
}'

test_endpoint "POST" "/api/v1/notifications/send" 200 "$test_data" "Testing send notification"

# Test 5: Get user notifications
test_endpoint "GET" "/api/v1/notifications/$TEST_USER_ID" 200 "" "Testing get user notifications"

# Test 6: Get user settings
test_endpoint "GET" "/api/v1/users/$TEST_USER_ID/settings" 200 "" "Testing get user settings"

# Test 7: Subscribe user
test_endpoint "POST" "/api/v1/users/$TEST_USER_ID/subscribe" 200 "" "Testing user subscription"

# Test 8: Unsubscribe user
test_endpoint "POST" "/api/v1/users/$TEST_USER_ID/unsubscribe" 200 "" "Testing user unsubscription"

# Test 9: Send another test notification with different priority
test_data_high='{
  "user_id": "'$TEST_USER_ID'",
  "notification_type": "trading_alert",
  "title": "High Priority Alert",
  "message": "This is a high priority trading alert",
  "priority": "high"
}'

test_endpoint "POST" "/api/v1/notifications/send" 200 "$test_data_high" "Testing high priority notification"

# Test 10: Test invalid endpoint (should return 404)
test_endpoint "GET" "/api/v1/invalid/endpoint" 404 "" "Testing invalid endpoint (should fail)"

echo "🎯 Test Summary"
echo "==============="
echo ""

# Check if service is properly configured
print_info "Checking service configuration..."

# Test if environment variables are set
if [ -f .env ]; then
    print_success ".env file exists"
    
    # Check critical settings
    if grep -q "TELEGRAM_BOT_TOKEN=" .env && ! grep -q "TELEGRAM_BOT_TOKEN=your-telegram-bot-token" .env; then
        print_success "Telegram bot token is configured"
    else
        print_fail "Telegram bot token not configured properly"
    fi
    
    if grep -q "AUTHORIZED_USERS=" .env; then
        print_success "Authorized users configured"
    else
        print_fail "Authorized users not configured"
    fi
else
    print_fail ".env file not found"
fi

# Test Redis connection
print_info "Testing Redis connection..."
if command -v redis-cli > /dev/null 2>&1; then
    if redis-cli ping > /dev/null 2>&1; then
        print_success "Redis is accessible"
    else
        print_fail "Redis is not accessible"
    fi
else
    print_info "redis-cli not available, skipping direct Redis test"
fi

# Final status check
print_info "Final service status check..."
if curl -s "$BASE_URL/api/v1/health/" > /dev/null; then
    print_success "✅ Notification Service is running and responding"
    
    # Get detailed status
    echo ""
    echo "📊 Service Status:"
    curl -s "$BASE_URL/api/v1/health/" | python -m json.tool
    
    echo ""
    echo "🔗 Useful URLs:"
    echo "  • API Documentation: $BASE_URL/docs"
    echo "  • Health Check: $BASE_URL/api/v1/health/"
    echo "  • Test Notification: curl -X POST $BASE_URL/api/v1/notifications/test/$TEST_USER_ID"
    
else
    print_fail "❌ Notification Service is not responding"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "  • Check if service is running: docker-compose ps"
    echo "  • View logs: docker-compose logs notification-service"
    echo "  • Restart service: docker-compose restart notification-service"
fi

echo ""
echo "🏁 Test completed!"
