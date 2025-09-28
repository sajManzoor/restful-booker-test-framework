import pytest
from clients.booking_client import BookingAPIClient
from config.environments import Config
from utils.assertions import APIAssertions


@pytest.mark.auth
class TestAuthentication:
    
    def test_valid_authentication(self, api_client: BookingAPIClient):
        """Test authentication with valid credentials"""
        credentials = Config.get_auth_credentials()
        token = api_client.get_auth_token(
            credentials['username'], 
            credentials['password']
        )
        APIAssertions.assert_auth_token(token)
    
    def test_invalid_username(self, api_client: BookingAPIClient):
        """Test authentication with invalid username"""
        credentials = Config.get_auth_credentials()
        with pytest.raises(Exception) as exc_info:
            api_client.get_auth_token("invalid_user", credentials['password'])
        assert "Authentication failed" in str(exc_info.value), f"Expected 'Authentication failed' in error message, got: {str(exc_info.value)}"
    
    def test_invalid_password(self, api_client: BookingAPIClient):
        """Test authentication with invalid password"""
        credentials = Config.get_auth_credentials()
        with pytest.raises(Exception) as exc_info:
            api_client.get_auth_token(credentials['username'], "wrong_password")
        
        assert "Authentication failed" in str(exc_info.value), f"Expected 'Authentication failed' in error message, got: {str(exc_info.value)}"
    
    def test_empty_credentials(self, api_client: BookingAPIClient):
        """Test authentication with empty credentials"""
        with pytest.raises(Exception) as exc_info:
            api_client.get_auth_token("", "")
        
        assert "Authentication failed" in str(exc_info.value), f"Expected 'Authentication failed' in error message, got: {str(exc_info.value)}"
