from datetime import datetime, timedelta


class BookingTestData:
    @staticmethod
    def valid_booking():
        """Generate valid booking data with future dates"""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        dates = BookingTestData.future_booking_dates()
        return {
            "firstname": f"John{unique_id}",
            "lastname": f"Doe{unique_id}",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": dates,
            "additionalneeds": "Breakfast"
        }

    @staticmethod
    def valid_booking_future_dates():
        checkin = datetime.now() + timedelta(days=1)
        checkout = datetime.now() + timedelta(days=3)

        booking = BookingTestData.valid_booking().copy()
        booking['bookingdates'].update({
            "checkin": checkin.strftime("%Y-%m-%d"),
            "checkout": checkout.strftime("%Y-%m-%d")
        })
        return booking

    @staticmethod
    def booking_with_specific_dates(checkin_date: str, checkout_date: str):
        """Create booking with specific dates for filtering tests"""
        booking = BookingTestData.valid_booking().copy()
        booking['bookingdates'].update({
            "checkin": checkin_date,
            "checkout": checkout_date
        })
        return booking

    @staticmethod
    def filter_test_booking_data():
        """Generate booking data for filter tests with dynamic names and future dates"""
        return BookingTestData.valid_booking()

    @staticmethod
    def filter_test_dates():
        """Test dates for parameterized filter testing"""
        return {
            "checkin_dates": ["2024-01-01", "2024-06-15", "2024-12-31", "2025-01-01", "2025-12-31"],
            "checkout_dates": ["2024-01-01", "2024-06-17", "2024-12-31", "2025-01-01", "2025-12-31"],
            "date_pairs": [
                ("2024-01-01", "2024-01-02"),
                ("2024-06-15", "2024-06-17"),
                ("2025-01-01", "2025-01-02")
            ]
        }

    @staticmethod
    def combined_filter_booking_data():
        """Booking data for combined name and date filtering"""
        return BookingTestData.valid_booking()

    @staticmethod
    def past_date_booking_data():
        """Booking data with past dates for negative filtering tests"""
        booking = BookingTestData.valid_booking().copy()
        booking['bookingdates'].update({
            "checkin": "2020-01-01",
            "checkout": "2020-01-05"
        })
        return booking

    @staticmethod
    def non_matching_names():
        """Names that should not match any existing bookings"""
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        return {
            "firstname": f"NonExistent{unique_id}",
            "lastname": f"Person{unique_id}"
        }

    @staticmethod
    def future_booking_dates():
        """Generate future booking dates (next week + 5 days)"""
        from datetime import datetime, timedelta
        checkin = datetime.now() + timedelta(days=7)  # Next week
        checkout = checkin + timedelta(days=5)  # 5 days later
        return {
            "checkin": checkin.strftime("%Y-%m-%d"),
            "checkout": checkout.strftime("%Y-%m-%d")
        }

    @staticmethod
    def updated_booking_data(original_data):
        """Generate updated booking data with different dates and details"""
        from datetime import datetime, timedelta
        import uuid

        # Parse original checkin date and add extra days to ensure difference
        original_checkin = datetime.strptime(original_data['bookingdates']['checkin'], "%Y-%m-%d")
        new_checkin = original_checkin + timedelta(days=10)  # 10 days later than original
        new_checkout = new_checkin + timedelta(days=7)  # 7 days stay

        unique_id = str(uuid.uuid4())[:6]

        return {
            "firstname": f"Updated{unique_id}",
            "lastname": f"Guest{unique_id}",
            "totalprice": original_data.get('totalprice', 100) + 50,  # Different price
            "depositpaid": not original_data.get('depositpaid', True),  # Opposite deposit status
            "bookingdates": {
                "checkin": new_checkin.strftime("%Y-%m-%d"),
                "checkout": new_checkout.strftime("%Y-%m-%d")
            },
            "additionalneeds": f"Updated needs {unique_id}"
        }
