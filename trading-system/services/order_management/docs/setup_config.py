#!/usr/bin/env python3
"""
Configuration helper to set up proper admin chat IDs
"""
import os
import json
from pathlib import Path

def setup_env_file():
    """Create or update .env file with proper configuration"""
    env_file = Path(".env")
    
    # Default configuration
    config = {
        "# Telegram Bot Configuration": "",
        "TELEGRAM_BOT_TOKEN": "7392190183:AAECmvDmW0c5QMA9JJ1xeKhQAzPSGD85U7A",
        "TELEGRAM_ADMIN_CHAT_IDS": "[]",  # Empty list for now
        "ENABLE_TELEGRAM_BOT": "true",
        "ENABLE_POLLING_MODE": "true",
        "ENABLE_WEBHOOK_MODE": "false",
        "ENABLE_ADMIN_NOTIFICATIONS": "false",  # Disable until chat IDs are configured
        "": "",
        "# API Configuration": "",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "DEBUG": "false",
        "LOG_LEVEL": "INFO",
    }
    
    # Write configuration to .env file
    with open(env_file, "w") as f:
        for key, value in config.items():
            if key.startswith("#") or key == "":
                f.write(f"{key}\n")
            else:
                f.write(f"{key}={value}\n")
    
    print(f"✅ Created {env_file} with default configuration")
    print("\n📋 Next steps:")
    print("1. Start a chat with your bot on Telegram")
    print("2. Send /start to get your chat ID")
    print("3. Add your chat ID to TELEGRAM_ADMIN_CHAT_IDS in .env")
    print("4. Set ENABLE_ADMIN_NOTIFICATIONS=true if you want startup notifications")

def get_chat_id_instructions():
    """Print instructions for getting chat ID"""
    print("\n🔍 How to get your Telegram chat ID:")
    print("1. Start a chat with @userinfobot on Telegram")
    print("2. Send any message to get your chat ID")
    print("3. Add it to .env file like: TELEGRAM_ADMIN_CHAT_IDS='[123456789]'")
    print("4. For multiple admins: TELEGRAM_ADMIN_CHAT_IDS='[123456789, 987654321]'")

if __name__ == "__main__":
    setup_env_file()
    get_chat_id_instructions()
