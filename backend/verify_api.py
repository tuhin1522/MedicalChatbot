#!/usr/bin/env python3
"""
API Verification Script
Quick check that all API components are importable
"""

import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

print("🔍 Verifying API Implementation...")
print("=" * 60)

# Test imports
tests = [
    ("Core module", "from src.core import config, logger"),
    ("Core exceptions", "from src.core.exceptions import ChatbotException, ServiceInitializationError"),
    ("API models (request)", "from src.api.models.request import ChatRequest, ResetRequest"),
    ("API models (response)", "from src.api.models.response import ChatResponse, HealthResponse"),
    ("API dependencies", "from src.api.dependencies import get_chatbot_config"),
    ("API middleware", "from src.api.middleware import ErrorHandlerMiddleware"),
    ("API routes (health)", "from src.api.routes.health import router as health_router"),
    ("API routes (chat)", "from src.api.routes.chat import router as chat_router"),
    ("API routes (admin)", "from src.api.routes.admin import router as admin_router"),
    ("FastAPI app", "from src.api import app"),
]

passed = 0
failed = 0

for test_name, import_statement in tests:
    try:
        exec(import_statement)
        print(f"✅ {test_name}")
        passed += 1
    except ImportError as e:
        print(f"❌ {test_name}: {e}")
        failed += 1
    except Exception as e:
        print(f"⚠️  {test_name}: {e}")
        failed += 1

print("=" * 60)
print(f"\n📊 Results: {passed} passed, {failed} failed")

if failed == 0:
    print("\n🎉 All imports successful! API is ready to use.")
    print("\n🚀 Next steps:")
    print("   1. Install dependencies: pip3 install --user fastapi uvicorn pydantic")
    print("   2. Start server: python3 main.py")
    print("   3. Open docs: http://localhost:8000/docs")
    sys.exit(0)
else:
    print("\n⚠️  Some imports failed. Please check:")
    print("   - Dependencies installed: pip3 install --user fastapi uvicorn pydantic")
    print("   - Python path is correct")
    print("   - All files are in place")
    sys.exit(1)
