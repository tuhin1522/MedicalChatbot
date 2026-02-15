"""
API Test Suite
Basic tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Medical Chatbot API"
        assert "version" in data
    
    def test_ping(self):
        """Test ping endpoint"""
        response = client.get("/health/ping")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["message"] == "pong"
    
    def test_version(self):
        """Test version endpoint"""
        response = client.get("/health/version")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert "llm_model" in data
    
    def test_uptime(self):
        """Test uptime endpoint"""
        response = client.get("/health/uptime")
        assert response.status_code == 200
        data = response.json()
        assert "uptime_seconds" in data
        assert "uptime_formatted" in data


class TestChatEndpoints:
    """Test chat endpoints"""
    
    def test_chat_validation(self):
        """Test chat endpoint with invalid input"""
        # Empty query
        response = client.post("/chat", json={"query": ""})
        assert response.status_code == 422  # Validation error
        
        # Query too short (after stripping)
        response = client.post("/chat", json={"query": "   "})
        assert response.status_code == 422
    
    def test_chat_status(self):
        """Test chat status endpoint"""
        response = client.get("/chat/status")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data


class TestAdminEndpoints:
    """Test admin endpoints"""
    
    def test_metrics(self):
        """Test metrics endpoint"""
        response = client.get("/admin/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_queries" in data
        assert "average_response_time" in data
    
    def test_database_info(self):
        """Test database info endpoint"""
        response = client.get("/admin/database/info")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "exists" in data


class TestErrorHandling:
    """Test error handling"""
    
    def test_not_found(self):
        """Test 404 error"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_method_not_allowed(self):
        """Test 405 error"""
        response = client.put("/health/ping")
        assert response.status_code == 405


def run_tests():
    """Run all tests"""
    print("Running API tests...")
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    run_tests()
