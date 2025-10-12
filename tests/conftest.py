import pytest
import os
import logging
from clients.booking_client import BookingAPIClient
from config.environments import Config
from utils.bug_reporter import BugReporter
from tests.data.test_data import BookingTestData

logger = logging.getLogger(__name__)
bug_reporter = BugReporter()


@pytest.fixture(scope="session", autouse=True)
def setup_test_session():
    """Setup test session"""
    yield

    # Generate reports at end of session only if there are bugs
    if bug_reporter.bugs:
        bug_reporter.generate_excel_report()
        logger.info(f"Generated bug report with {len(bug_reporter.bugs)} bugs")
    else:
        logger.info("No bugs detected - skipping report generation")


@pytest.fixture(scope="session")
def config():
    """Configuration fixture"""
    return Config()


@pytest.fixture(scope="session")
def api_client(config):
    """Base API client fixture"""
    return BookingAPIClient(config)


@pytest.fixture
def booking_factory(api_client):
    """Factory fixture for creating bookings with automatic cleanup"""
    created_bookings = []

    def _create_booking(booking_data=None):
        if booking_data is None:
            booking_data = BookingTestData.valid_booking()

        booking_response = api_client.create_booking(booking_data)
        booking_id = booking_response.bookingid
        created_bookings.append(booking_id)
        return booking_response, booking_data

    yield _create_booking

    # Cleanup all created bookings
    for booking_id in created_bookings:
        try:
            api_client.delete_booking(booking_id)
        except Exception:
            pass  # Ignore cleanup errors


@pytest.fixture
def standard_booking(booking_factory):
    """Standard booking for tests"""
    return booking_factory()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results and automatically report bugs"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

    # Only process failures in the call phase (actual test execution)
    if call.when == "call" and rep.failed:
        # Add bug automatically using the test item for better description
        bug_reporter.add_auto_detected_bug(
            test_name=item.name,
            failure_message=str(rep.longrepr),
            test_item=item
        )
