#!/usr/bin/env python3
"""
Test OTP Flow
Test the complete OTP authentication flow
"""

import asyncio
import json
from app.services.fc_trading_service import fc_trading_service
from app.services.async_fc_trading_service import AsyncFCTradingService

async def test_otp_flow():
    """Test the complete OTP authentication flow"""
    print("🧪 Testing OTP Authentication Flow...")
    
    # Test 1: Direct FC Trading Service
    print("\n1️⃣ Testing Direct FC Trading Service:")
    
    # Get OTP
    otp_result = fc_trading_service.get_otp()
    otp_data = json.loads(otp_result)
    print(f"   📱 OTP Request: {otp_data['success']} - {otp_data['message']}")
    
    if otp_data.get('data', {}).get('mock_code'):
        mock_code = otp_data['data']['mock_code']
        print(f"   🔢 Mock OTP Code: {mock_code}")
    
    # Verify code
    verify_result = fc_trading_service.verify_code('123456')
    verify_data = json.loads(verify_result)
    print(f"   ✅ Verification: {verify_data['success']} - {verify_data['message']}")
    
    # Test 2: Async FC Trading Service  
    print("\n2️⃣ Testing Async FC Trading Service:")
    async_service = AsyncFCTradingService()
    test_user_id = "test_user_123"
    
    # Get OTP async
    async_otp_result = await async_service.get_otp(test_user_id)
    print(f"   📱 Async OTP Request: {async_otp_result['success']} - {async_otp_result['message']}")
    
    # Verify code async
    async_verify_result = await async_service.verify_otp(test_user_id, '123456')
    print(f"   ✅ Async Verification: {async_verify_result['success']} - {async_verify_result['message']}")
    
    # Test 3: Invalid code
    print("\n3️⃣ Testing Invalid Code:")
    invalid_result = fc_trading_service.verify_code('invalid')
    invalid_data = json.loads(invalid_result)
    print(f"   ❌ Invalid Code: {invalid_data['success']} - {invalid_data['message']}")
    
    print("\n✅ OTP Flow Test Complete!")
    
    return {
        'direct_otp': otp_data['success'],
        'direct_verify': verify_data['success'], 
        'async_otp': async_otp_result['success'],
        'async_verify': async_verify_result['success'],
        'invalid_code': not invalid_data['success']  # Should be false (failure expected)
    }

if __name__ == "__main__":
    result = asyncio.run(test_otp_flow())
    print(f"\n📊 Test Results: {result}")
    all_passed = all(result.values())
    print(f"🎯 Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
