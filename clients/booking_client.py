from typing import List, Optional, Dict, Any
from clients.base_client import BaseAPIClient
from config.environments import Config
from models.booking import Booking, BookingResponse, AuthRequest, AuthResponse, BookingDates
from datetime import date


class BookingAPIClient(BaseAPIClient):

    def __init__(self, config: Config = None, timeout: int = 30):
        if not config:
            config = Config()

        base_url = Config.get_base_url()
        super().__init__(base_url, timeout)
        self.config = config
        self._auth_token = None

    def get_auth_token(self, username: str, password: str) -> str:
        """Get authentication token"""
        auth_request = AuthRequest(username=username, password=password)
        response = self._make_request('POST', '/auth', json=auth_request.to_dict())

        if response.status_code == 200:
            response_data = response.json()
            if 'token' not in response_data:
                raise Exception(f"Authentication failed: No token in response")
            self._auth_token = response_data['token']
            return self._auth_token
        else:
            raise Exception(f"Authentication failed: {response.status_code} - {response.text}")

    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers, obtaining token if needed"""
        if not self._auth_token:
            credentials = Config.get_auth_credentials()
            self.get_auth_token(credentials['username'], credentials['password'])

        return {
            'Cookie': f'token={self._auth_token}',
            'Authorization': f'Basic {self._auth_token}'
        }

    def get_all_booking_ids(self) -> List[int]:
        """Get all booking IDs"""
        return self.get_booking_ids()

    def get_booking_ids(self, firstname: Optional[str] = None,
                        lastname: Optional[str] = None,
                        checkin: Optional[str] = None,
                        checkout: Optional[str] = None) -> List[int]:
        """Get list of booking IDs with optional filters"""
        params = {k: v for k, v in locals().items()
                 if k != 'self' and v is not None}
        response = self._make_request('GET', '/booking', params=params)

        if response.status_code == 200:
            return [booking['bookingid'] for booking in response.json()]
        else:
            raise Exception(f"Failed to get booking IDs: {response.status_code} - {response.text}")

    def filter_bookings_by_name(self, firstname: str = None, lastname: str = None) -> List[int]:
        """Filter bookings by name (legacy method)"""
        return self.get_booking_ids(firstname=firstname, lastname=lastname)

    def filter_bookings_by_dates(self, checkin: str = None, checkout: str = None) -> List[int]:
        """Filter bookings by check-in/check-out dates"""
        return self.get_booking_ids(checkin=checkin, checkout=checkout)

    def get_booking_by_id(self, booking_id: int) -> Booking:
        """Get booking by ID"""
        response = self._make_request('GET', f'/booking/{booking_id}')

        if response.status_code == 200:
            return Booking.from_dict(response.json())
        else:
            raise Exception(f"Failed to get booking {booking_id}: {response.status_code} - {response.text}")

    def create_booking(self, booking_data: Dict[str, Any]) -> BookingResponse:
        """Create a new booking"""
        response = self._make_request('POST', '/booking', json=booking_data)

        if response.status_code == 200:
            data = response.json()
            booking = Booking.from_dict(data['booking'])
            return BookingResponse(bookingid=data['bookingid'], booking=booking)
        else:
            raise Exception(f"Failed to create booking: {response.status_code} - {response.text}")

    def update_booking(self, booking_id: int, booking_data: Dict[str, Any]) -> Booking:
        """Update existing booking"""
        headers = self._get_auth_headers()

        response = self._make_request('PUT', f'/booking/{booking_id}',
                                    json=booking_data, headers=headers)

        if response.status_code == 200:
            return Booking.from_dict(response.json())
        else:
            raise Exception(f"Failed to update booking {booking_id}: {response.status_code} - {response.text}")

    def partial_update_booking(self, booking_id: int, updates: Dict[str, Any]) -> Booking:
        """Partially update existing booking"""
        headers = self._get_auth_headers()

        response = self._make_request('PATCH', f'/booking/{booking_id}',
                                    json=updates, headers=headers)

        if response.status_code == 200:
            return Booking.from_dict(response.json())
        else:
            raise Exception(f"Failed to partially update booking {booking_id}: {response.status_code} - {response.text}")

    def delete_booking(self, booking_id: int) -> bool:
        """Delete booking"""
        headers = self._get_auth_headers()

        response = self._make_request('DELETE', f'/booking/{booking_id}', headers=headers)

        return response.status_code in [200, 201, 204]

    def update_booking_without_auth(self, booking_id: int, booking_data: Dict[str, Any]) -> Booking:
        """Update booking without authentication (for negative testing)"""
        response = self._make_request('PUT', f'/booking/{booking_id}', json=booking_data)

        if response.status_code == 200:
            return Booking.from_dict(response.json())
        else:
            raise Exception(f"Failed to update booking {booking_id}: {response.status_code} - {response.text}")

    def delete_booking_without_auth(self, booking_id: int) -> bool:
        """Delete booking without authentication (for negative testing)"""
        response = self._make_request('DELETE', f'/booking/{booking_id}')

        if response.status_code in [200, 201, 204]:
            return True
        else:
            raise Exception(f"Failed to delete booking {booking_id}: {response.status_code} - {response.text}")
