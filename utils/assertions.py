from typing import Dict, Any


class APIAssertions:
    @staticmethod
    def assert_booking_structure(booking_data: Dict[str, Any]):
        """Validate booking data has required structure"""
        required_fields = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates']
        for field in required_fields:
            assert field in booking_data, f"Missing required field: {field}"
        
        # Validate bookingdates structure
        if 'bookingdates' in booking_data:
            booking_dates = booking_data['bookingdates']
            assert 'checkin' in booking_dates, "Missing checkin date"
            assert 'checkout' in booking_dates, "Missing checkout date"
    
    @staticmethod
    def assert_booking_equality(booking1: Dict[str, Any], booking2: Dict[str, Any], ignore_fields: list = None):
        """Compare two booking objects for equality, optionally ignoring certain fields"""
        ignore_fields = ignore_fields or []
        for key, value in booking1.items():
            if key not in ignore_fields:
                assert key in booking2, f"Field '{key}' missing in second booking"
                assert booking2[key] == value, f"Field '{key}' mismatch: {value} != {booking2[key]}"
    
    @staticmethod
    def assert_auth_token(token):
        """Validate authentication token format and content"""
        assert token is not None, "Token should not be None"
        assert len(token) > 0, "Token should not be empty"
        assert isinstance(token, str), "Token should be a string"
    
    @staticmethod
    def assert_booking_id(booking_id):
        """Validate booking ID format and value"""
        assert booking_id is not None, "Booking ID should not be None"
        assert isinstance(booking_id, int), "Booking ID should be an integer"
        assert booking_id > 0, "Booking ID should be positive"
