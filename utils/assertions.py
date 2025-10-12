from typing import Dict, Any, Union
from models.booking import Booking


class APIAssertions:
    @staticmethod
    def assert_booking_structure(booking_data: Booking):
        """Validate booking data has required structure"""
        assert booking_data.firstname is not None
        assert booking_data.lastname is not None
        assert booking_data.totalprice is not None
        assert booking_data.depositpaid is not None
        assert booking_data.bookingdates is not None
        assert booking_data.bookingdates.checkin is not None
        assert booking_data.bookingdates.checkout is not None

    @staticmethod
    def assert_booking_equality(booking1: Union[Dict[str, Any], Booking], booking2: Union[Dict[str, Any], Booking], ignore_fields: list = None):
        """Compare two booking objects for equality, optionally ignoring certain fields"""
        ignore_fields = ignore_fields or []

        # Convert models to dicts for comparison
        dict1 = booking1.to_dict() if isinstance(booking1, Booking) else booking1
        dict2 = booking2.to_dict() if isinstance(booking2, Booking) else booking2

        for key, value in dict1.items():
            if key not in ignore_fields:
                assert key in dict2, f"Field '{key}' missing in second booking"
                assert dict2[key] == value, f"Field '{key}' mismatch: {value} != {dict2[key]}"

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
