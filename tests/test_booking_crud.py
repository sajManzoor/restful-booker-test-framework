import pytest
from clients.booking_client import BookingAPIClient
from tests.data.test_data import BookingTestData
from utils.assertions import APIAssertions

@pytest.mark.booking
class TestBookingCRUD:

    @pytest.mark.smoke
    def test_create_booking(self, booking_factory):
        """Test creating a new booking"""
        booking_response, booking_data = booking_factory()
        APIAssertions.assert_booking_id(booking_response.bookingid)

    @pytest.mark.smoke
    def test_get_booking_by_id(self, api_client, standard_booking):
        """Test retrieving a booking by ID"""
        booking_response, original_data = standard_booking
        booking_id = booking_response.bookingid
        retrieved_booking = api_client.get_booking_by_id(booking_id)

        APIAssertions.assert_booking_structure(retrieved_booking)
        APIAssertions.assert_booking_equality(original_data, retrieved_booking)

    def test_get_all_booking_ids(self, api_client):
        """Test retrieving all booking IDs"""
        booking_ids = api_client.get_all_booking_ids()

        assert isinstance(booking_ids, list), f"Expected list, got {type(booking_ids).__name__}: {booking_ids}"
        assert len(booking_ids) > 0, f"No booking IDs returned, expected at least 1"

        check_count = min(5, len(booking_ids))
        for booking_id in booking_ids[:check_count]:
            APIAssertions.assert_booking_id(booking_id)
            retrieved_booking = api_client.get_booking_by_id(booking_id)
            APIAssertions.assert_booking_structure(retrieved_booking)

    def test_update_booking(self, api_client, standard_booking):
        """Test updating a complete booking"""
        booking_response, original_data = standard_booking
        booking_id = booking_response.bookingid

        updated_data = BookingTestData.valid_booking_future_dates()
        api_client.update_booking(booking_id, updated_data)

        retrieved = api_client.get_booking_by_id(booking_id)
        APIAssertions.assert_booking_structure(retrieved)
        APIAssertions.assert_booking_equality(updated_data, retrieved)

    def test_partial_update_booking(self, api_client, standard_booking):
        """Test partially updating a booking"""
        booking_response, original_data = standard_booking
        booking_id = booking_response.bookingid

        # Create partial update with modified original values
        partial_data = {
            "firstname": original_data['firstname'] + "_Updated",
            "totalprice": original_data['totalprice'] + 100
        }
        api_client.partial_update_booking(booking_id, partial_data)

        retrieved = api_client.get_booking_by_id(booking_id)
        APIAssertions.assert_booking_structure(retrieved)

        # Create expected data by merging original with updates
        expected_data = original_data.copy()
        expected_data.update(partial_data)

        APIAssertions.assert_booking_equality(expected_data, retrieved)

    def test_delete_booking(self, api_client, standard_booking):
        """Test deleting a booking"""
        booking_response, _ = standard_booking
        booking_id = booking_response.bookingid

        retrieved = api_client.get_booking_by_id(booking_id)
        assert retrieved is not None

        api_client.delete_booking(booking_id)

        with pytest.raises(Exception):
            api_client.get_booking_by_id(booking_id)

