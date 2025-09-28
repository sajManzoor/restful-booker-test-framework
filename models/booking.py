from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class BookingDates:
    checkin: date
    checkout: date
    
    def to_dict(self):
        return {
            'checkin': self.checkin.isoformat(),
            'checkout': self.checkout.isoformat()
        }

@dataclass
class Booking:
    firstname: str
    lastname: str
    totalprice: int
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None
    
    def to_dict(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'totalprice': self.totalprice,
            'depositpaid': self.depositpaid,
            'bookingdates': self.bookingdates.to_dict(),
            'additionalneeds': self.additionalneeds
        }
    
    @classmethod
    def from_dict(cls, data):
        booking_dates = BookingDates(
            checkin=date.fromisoformat(data['bookingdates']['checkin']),
            checkout=date.fromisoformat(data['bookingdates']['checkout'])
        )
        return cls(
            firstname=data['firstname'],
            lastname=data['lastname'],
            totalprice=data['totalprice'],
            depositpaid=data['depositpaid'],
            bookingdates=booking_dates,
            additionalneeds=data.get('additionalneeds')
        )

@dataclass
class BookingResponse:
    bookingid: int
    booking: Booking

@dataclass
class AuthRequest:
    username: str
    password: str
    
    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password
        }

@dataclass
class AuthResponse:
    token: str
