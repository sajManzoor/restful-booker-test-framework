import pytest
import logging
from datetime import datetime, timedelta
from clients.booking_client import BookingAPIClient
from tests.data.test_data import BookingTestData

logger = logging.getLogger(__name__)


@pytest.mark.booking
@pytest.mark.regression
class TestBookingFilters:
    """Test booking filtering functionality"""
    
    @pytest.mark.parametrize("checkin_date", BookingTestData.filter_test_dates()["checkin_dates"])
    def test_filter_by_checkin_date(self, api_client, booking_factory, checkin_date):
        """Test filtering bookings by check-in date - exposes API inconsistencies"""
        # Create booking with the parameterized checkin date
        booking_data = BookingTestData.filter_test_booking_data()
        booking_data['bookingdates']['checkin'] = checkin_date
        
        booking_id, _ = booking_factory(booking_data)
        
        filtered_ids = api_client.filter_bookings_by_dates(checkin=checkin_date)
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"

    
    @pytest.mark.parametrize("checkout_date", BookingTestData.filter_test_dates()["checkout_dates"])
    def test_filter_by_checkout_date(self, api_client, booking_factory, checkout_date):
        """Test filtering bookings by check-out date - exposes API inconsistencies"""
        # Create booking with the parameterized checkout date
        booking_data = BookingTestData.filter_test_booking_data()
        booking_data['bookingdates']['checkout'] = checkout_date
        
        booking_id, _ = booking_factory(booking_data)
        
        filtered_ids = api_client.filter_bookings_by_dates(checkout=checkout_date)
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in checkout filter results for {checkout_date}"
    
    @pytest.mark.parametrize("checkin_date,checkout_date", BookingTestData.filter_test_dates()["date_pairs"])
    def test_filter_by_both_dates(self, api_client, booking_factory, checkin_date, checkout_date):
        """Test filtering by both dates - exposes API inconsistencies"""
        # Create booking with the parameterized dates
        booking_data = BookingTestData.filter_test_booking_data()
        booking_data['bookingdates']['checkin'] = checkin_date
        booking_data['bookingdates']['checkout'] = checkout_date
        
        booking_id, _ = booking_factory(booking_data)
        
        filtered_ids = api_client.filter_bookings_by_dates(checkin=checkin_date, checkout=checkout_date)
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in date range filter for {checkin_date} to {checkout_date}"

    def test_filter_by_first_name_only(self, api_client, booking_factory):
        """Test filtering bookings by name only"""
        booking_data = BookingTestData.filter_test_booking_data()
        booking_id, _ = booking_factory(booking_data)

        # Filter by firstname only
        filtered_ids = api_client.filter_bookings_by_name(
            firstname=booking_data['firstname']
        )

        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in firstname filter for '{booking_data['firstname']}'"

    def test_filter_by_last_name_only(self, api_client, booking_factory):
        """Test filtering bookings by name only"""
        booking_data = BookingTestData.filter_test_booking_data()
        booking_id, _ = booking_factory(booking_data)

        # Filter by lastname only
        filtered_ids = api_client.filter_bookings_by_name(
            lastname=booking_data['lastname']
        )

        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in lastname filter for '{booking_data['lastname']}'"

    def test_filter_by_full_name(self, api_client, booking_factory):
        """Test filtering bookings by both first and last name"""
        booking_data = BookingTestData.filter_test_booking_data()
        booking_id, _ = booking_factory(booking_data)

        # Filter by both first and lastname
        filtered_ids = api_client.filter_bookings_by_name(
            firstname=booking_data['firstname'],
            lastname=booking_data['lastname']
        )

        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in full name filter for '{booking_data['firstname']} {booking_data['lastname']}'"

    def test_filter_by_name_and_dates(self, api_client, booking_factory):
        """Test filtering bookings by name and dates combined"""
        booking_data = BookingTestData.combined_filter_booking_data()
        booking_id, _ = booking_factory(booking_data)
        
        filtered_ids = api_client.get_booking_ids(
            firstname=booking_data['firstname'],
            lastname=booking_data['lastname'],
            checkin=booking_data['bookingdates']['checkin'],
            checkout=booking_data['bookingdates']['checkout']
        )
        
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in combined name+date filter"
    
    @pytest.mark.critical
    def test_filter_date_boundary_conditions(self, api_client, booking_factory):
        """Test date filtering with boundary conditions"""
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        booking_data = BookingTestData.booking_with_specific_dates(today, tomorrow)
        booking_id, _ = booking_factory(booking_data)
        
        filtered_ids = api_client.filter_bookings_by_dates(checkin=today)
        
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id in filtered_ids, f"Booking {booking_id} not found in boundary date filter for {today}"
    
    def test_empty_filter_parameters(self, api_client):
        """Test filtering with empty parameters"""
        try:
            filtered_ids = api_client.get_booking_ids(firstname="", lastname="")
            assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        except Exception as e:
            logger.warning(f"Empty string filter failed: {e}")
        
        all_bookings = api_client.get_booking_ids()
        none_filtered = api_client.get_booking_ids(firstname=None, lastname=None)
        
        assert len(all_bookings) == len(none_filtered), f"Empty filter inconsistency: all_bookings={len(all_bookings)} vs none_filtered={len(none_filtered)}"
    
    def test_filter_should_exclude_booking_by_checkin(self, api_client, booking_factory):
        """Test that bookings are excluded when they don't match checkin filter"""
        booking_data = BookingTestData.past_date_booking_data()
        booking_id, _ = booking_factory(booking_data)
        
        # Get booking's checkin date and add 1 year to ensure it's in the future
        from datetime import datetime, timedelta
        booking_checkin = datetime.strptime(booking_data['bookingdates']['checkin'], "%Y-%m-%d")
        future_checkin = (booking_checkin + timedelta(days=365)).strftime("%Y-%m-%d")
        
        filtered_ids = api_client.filter_bookings_by_dates(checkin=future_checkin)
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"

        assert booking_id not in filtered_ids, ("Booking with past checkin found in future-date "
                                                "filter - filtering broken")
    
    def test_filter_should_exclude_booking_by_checkout(self, api_client, booking_factory):
        """Test that bookings are excluded when they don't match checkout filter"""
        booking_data = BookingTestData.past_date_booking_data()
        booking_id, _ = booking_factory(booking_data)

        from datetime import datetime, timedelta
        booking_checkout = datetime.strptime(booking_data['bookingdates']['checkout'], "%Y-%m-%d")
        future_checkout = (booking_checkout + timedelta(days=365)).strftime("%Y-%m-%d")
        
        filtered_ids = api_client.filter_bookings_by_dates(checkout=future_checkout)
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id not in filtered_ids, ("Booking with past checkout found in "
                                                "future-date filter - filtering broken")

    def test_filter_by_full_name_should_exclude_booking(self, api_client, booking_factory):
        """Test that bookings are excluded when they don't match full name filter"""
        booking_data = BookingTestData.filter_test_booking_data()
        booking_id, _ = booking_factory(booking_data)
        
        # Filter by completely different names - our booking should NOT be included
        non_matching = BookingTestData.non_matching_names()
        filtered_ids = api_client.filter_bookings_by_name(
            firstname=non_matching['firstname'],
            lastname=non_matching['lastname']
        )
        
        assert isinstance(filtered_ids, list), f"Expected list, got {type(filtered_ids).__name__}: {filtered_ids}"
        assert booking_id not in filtered_ids, ("Booking found in filter results for different "
                                                "names - name filtering broken")
