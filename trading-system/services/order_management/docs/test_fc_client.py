#!/usr/bin/env python3
"""
Test FC Trading Client initialization
"""

from ssi_fctrading import FCTradingClient
from app.config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fc_client():
    """Test FC Trading client initialization"""
    try:
        print("🔍 Testing FC Trading Client initialization...")
        print(f"URL: {settings.fc_trading_url}")
        print(f"Consumer ID: {settings.consumer_id}")
        print(f"Two FA Type: {settings.two_fa_type}")
        
        # Try to initialize client
        client = FCTradingClient(
            url=settings.fc_trading_url,
            consumer_id=settings.consumer_id,
            consumer_secret=settings.consumer_secret,
            private_key=settings.private_key,
            twoFAType=settings.two_fa_type
        )
        
        print("✅ FC Trading client initialized successfully!")
        
        # Test get_otp method
        print("📱 Testing get_otp...")
        result = client.get_otp()
        print(f"OTP Result: {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_fc_client()
