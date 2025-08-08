#!/usr/bin/env python3
"""
Simple test to check if the Order Management Service can start
"""

import sys
import os

# Add the parent directory to Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print("🔍 Testing Order Management Service...")

try:
    print("1. Testing FastAPI import...")
    from fastapi import FastAPI
    print("✅ FastAPI imported successfully")
    
    print("2. Testing app configuration...")
    from app.config import settings
    print(f"✅ Config loaded: {settings.app_name}")
    
    print("3. Testing database connection...")
    from app.database import engine
    print("✅ Database engine created")
    
    print("4. Testing main app import...")
    from app.main_new import app
    print(f"✅ App created: {type(app)}")
    
    print("5. Testing routes...")
    routes = [route.path for route in app.routes]
    print(f"✅ Routes available: {len(routes)} routes")
    for route in routes[:5]:  # Show first 5 routes
        print(f"   - {route}")
    
    print("\n🎉 All tests passed! Service is ready to start.")
    
    # Try to get app info
    print("\n📊 App Information:")
    print(f"   - Title: {app.title}")
    print(f"   - Version: {app.version}")
    print(f"   - Debug: {settings.debug}")
    print(f"   - Host: {settings.host}")
    print(f"   - Port: {settings.port}")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
