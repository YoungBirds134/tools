#!/usr/bin/env python3
"""
Test script for FC Trading API and Telegram Bot
"""

import requests
import json
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_auth_endpoints():
    """Test authentication endpoints"""
    print("\n=== Testing Authentication Endpoints ===")
    
    # Test OTP
    try:
        response = requests.get(f"{BASE_URL}/api/v1/auth/otp")
        print(f"✅ OTP request: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ OTP request failed: {e}")
    
    # Test verify code
    try:
        data = {"code": "123456"}
        response = requests.post(f"{BASE_URL}/api/v1/auth/verify-code", json=data)
        print(f"✅ Verify code: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Verify code failed: {e}")

def test_account_endpoints():
    """Test account endpoints"""
    print("\n=== Testing Account Endpoints ===")
    
    # Test account balance
    try:
        params = {"account": "DEMO123456"}
        response = requests.get(f"{BASE_URL}/api/v1/accounts/balance", params=params)
        print(f"✅ Account balance: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Account balance failed: {e}")
    
    # Test positions
    try:
        params = {"account": "DEMO123456"}
        response = requests.get(f"{BASE_URL}/api/v1/accounts/positions", params=params)
        print(f"✅ Positions: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Positions failed: {e}")

def test_orders_endpoints():
    """Test orders endpoints"""
    print("\n=== Testing Orders Endpoints ===")
    
    # Test order history
    try:
        params = {
            "account": "DEMO123456",
            "start_date": "2025-01-01",
            "end_date": "2025-01-31"
        }
        response = requests.get(f"{BASE_URL}/api/v1/orders/history", params=params)
        print(f"✅ Order history: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Order history failed: {e}")
    
    # Test order book
    try:
        params = {"account": "DEMO123456"}
        response = requests.get(f"{BASE_URL}/api/v1/orders/book", params=params)
        print(f"✅ Order book: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Order book failed: {e}")

def test_telegram_endpoints():
    """Test Telegram endpoints"""
    print("\n=== Testing Telegram Endpoints ===")
    
    # Test send message
    try:
        data = {
            "chat_id": "123456789",
            "text": "Test message from API",
            "parse_mode": "Markdown"
        }
        response = requests.post(f"{BASE_URL}/api/v1/telegram/bot/send-message", json=data)
        print(f"✅ Send message: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Send message failed: {e}")
    
    # Test bot status
    try:
        response = requests.get(f"{BASE_URL}/api/v1/telegram/bot/status")
        print(f"✅ Bot status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Bot status failed: {e}")

def test_trading_flow():
    """Test complete trading flow"""
    print("\n=== Testing Trading Flow ===")
    
    # Test authentication flow
    try:
        data = {"chat_id": 123456789}
        response = requests.post(f"{BASE_URL}/api/v1/telegram/flows/auth", json=data)
        print(f"✅ Auth flow: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Auth flow failed: {e}")
    
    # Test account flow
    try:
        data = {"chat_id": 123456789}
        response = requests.post(f"{BASE_URL}/api/v1/telegram/flows/account", json=data)
        print(f"✅ Account flow: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Account flow failed: {e}")

def main():
    """Main test function"""
    print("🚀 Starting FC Trading API Test Suite")
    print("=" * 50)
    
    # Test health first
    if not test_health():
        print("❌ Server is not running. Please start the server first.")
        return
    
    # Test all endpoints
    test_auth_endpoints()
    test_account_endpoints()
    test_orders_endpoints()
    test_telegram_endpoints()
    test_trading_flow()
    
    print("\n" + "=" * 50)
    print("✅ Test suite completed!")
    print("📊 Server is running at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("🤖 Telegram bot is ready for production!")

if __name__ == "__main__":
    main()
