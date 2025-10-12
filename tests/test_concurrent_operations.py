import pytest
from concurrent.futures import ThreadPoolExecutor
from clients.booking_client import BookingAPIClient
from tests.data.test_data import BookingTestData
from utils.assertions import APIAssertions
from utils.concurrency import ConcurrencyUtils


@pytest.mark.concurrent
class TestConcurrentOperations:
    """Test concurrent API operations"""

    def test_concurrent_booking_operations(self, api_client, booking_factory):
        """Test concurrent booking create and read operations"""

        # Create operations
        def create_booking():
            booking_data = BookingTestData.valid_booking()
            booking_response, _ = booking_factory(booking_data)
            return booking_response.bookingid, booking_data

        # Run 3 concurrent creates
        create_ops = [create_booking for _ in range(3)]
        results = ConcurrencyUtils.run_concurrent_operations(create_ops)

        # Validate all creations succeeded
        assert len(results) == 3
        booking_ids = [result[0] for result in results]

        for booking_id in booking_ids:
            APIAssertions.assert_booking_id(booking_id)

        # Create concurrent read operations
        def read_booking(bid):
            return api_client.get_booking_by_id(bid)

        # Run concurrent reads
        read_ops = [lambda bid=bid: read_booking(bid) for bid in booking_ids]
        retrieved_bookings = ConcurrencyUtils.run_concurrent_operations(read_ops)

        # Validate all reads succeeded
        assert len(retrieved_bookings) == 3
        for booking in retrieved_bookings:
            APIAssertions.assert_booking_structure(booking)

    def test_concurrent_read_write_operations(self, api_client, booking_factory):
        """Test concurrent read and write operations on same booking"""
        booking_response, original_data = booking_factory()
        booking_id = booking_response.bookingid

        def read_booking():
            return api_client.get_booking_by_id(booking_id)

        def update_booking():
            new_booking_data = BookingTestData.updated_booking_data(original_data)
            api_client.update_booking(booking_id, new_booking_data)
            return new_booking_data

        # Run read and write concurrently
        with ThreadPoolExecutor(max_workers=2) as executor:
            read_future = executor.submit(read_booking)
            write_future = executor.submit(update_booking)

            # Wait for both operations to complete
            read_future.result()
            updated_data = write_future.result()

        # Verify no corruption occurred and update was successful
        final_booking = api_client.get_booking_by_id(booking_id)
        assert final_booking is not None
        APIAssertions.assert_booking_structure(final_booking)
        APIAssertions.assert_booking_equality(final_booking, updated_data)
