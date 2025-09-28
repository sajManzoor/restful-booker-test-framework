import pytest

@pytest.mark.smoke
@pytest.mark.health
class TestHealthEndpoint:
    """Test essential health check endpoints"""
    
    def test_ping_health_check(self, api_client):
        """Test the /ping health check endpoint"""
        is_healthy = api_client.ping_health_check()
        assert is_healthy, "API health check failed - service may be down"
