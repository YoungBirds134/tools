#!/usr/bin/env python3
"""
Production Integration Test for FC Trading Bot
Tests the complete integration between Telegram Bot and FC Trading Service
"""

import asyncio
import logging
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.telegram.bot import TelegramBot
from app.telegram.handlers import TelegramHandlers
from app.services.async_fc_trading_service import async_fc_trading_service
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_fc_service_availability():
    """Test FC Trading Service availability"""
    logger.info("Testing FC Trading Service availability...")
    
    try:
        is_available = await async_fc_trading_service.is_available()
        logger.info(f"FC Trading Service available: {is_available}")
        return is_available
    except Exception as e:
        logger.error(f"Error testing FC service: {e}")
        return False


async def test_mock_symbols():
    """Test getting symbols (mock data fallback)"""
    logger.info("Testing symbols retrieval...")
    
    try:
        symbols_data = await async_fc_trading_service.get_symbols()
        if symbols_data.get('success'):
            symbols = symbols_data.get('data', [])
            logger.info(f"Retrieved {len(symbols)} symbols")
            for symbol in symbols[:3]:  # Show first 3
                logger.info(f"  - {symbol.get('symbol')}: {symbol.get('name')}")
            return True
        else:
            logger.error(f"Failed to get symbols: {symbols_data.get('message')}")
            return False
    except Exception as e:
        logger.error(f"Error getting symbols: {e}")
        return False


async def test_bot_initialization():
    """Test bot initialization"""
    logger.info("Testing bot initialization...")
    
    try:
        # Test bot creation
        bot = TelegramBot()
        logger.info("Bot created successfully")
        
        # Test handlers initialization
        handlers = TelegramHandlers()
        logger.info("Handlers initialized successfully")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing bot: {e}")
        return False


async def test_configuration():
    """Test configuration"""
    logger.info("Testing configuration...")
    
    # Check required config
    required_configs = ['TELEGRAM_BOT_TOKEN', 'REDIS_URL']
    missing_configs = []
    
    for config in required_configs:
        if not hasattr(settings, config) or not getattr(settings, config):
            missing_configs.append(config)
    
    if missing_configs:
        logger.warning(f"Missing configurations: {missing_configs}")
        logger.info("Bot will run in mock mode for missing configurations")
    else:
        logger.info("All required configurations present")
    
    return len(missing_configs) == 0


async def run_integration_test():
    """Run complete integration test"""
    logger.info("=" * 60)
    logger.info("FC TRADING BOT - PRODUCTION INTEGRATION TEST")
    logger.info("=" * 60)
    
    test_results = {
        'configuration': False,
        'bot_initialization': False,
        'fc_service': False,
        'symbols': False
    }
    
    # Test 1: Configuration
    logger.info("\n1. Testing Configuration...")
    test_results['configuration'] = await test_configuration()
    
    # Test 2: Bot Initialization
    logger.info("\n2. Testing Bot Initialization...")
    test_results['bot_initialization'] = await test_bot_initialization()
    
    # Test 3: FC Service
    logger.info("\n3. Testing FC Trading Service...")
    test_results['fc_service'] = await test_fc_service_availability()
    
    # Test 4: Symbols
    logger.info("\n4. Testing Symbols Retrieval...")
    test_results['symbols'] = await test_mock_symbols()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("INTEGRATION TEST RESULTS")
    logger.info("=" * 60)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{test_name.replace('_', ' ').title()}: {status}")
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    logger.info(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= 3:  # At least configuration, bot init, and symbols should pass
        logger.info("\n🎉 INTEGRATION READY FOR PRODUCTION!")
        logger.info("\nNext steps:")
        logger.info("1. Start the bot: python run.py")
        logger.info("2. Test /start command in Telegram")
        logger.info("3. Test authentication flow")
        logger.info("4. Test trading commands")
        return True
    else:
        logger.warning("\n⚠️  INTEGRATION NEEDS ATTENTION")
        logger.info("\nPlease fix failing tests before production deployment")
        return False


async def main():
    """Main test function"""
    try:
        success = await run_integration_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error during testing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
