# Appointment Model

# Import dependencies
from server.database import db
from datetime import time

# Import Enum class from the enum module
from enum import Enum

# Import AppointmentStatus Enum to avoid circular import
from . import AppointmentStatus


# Define model
class Appointment(db.Model):
    # Define status options using Enum
    class AppointmentStatus(Enum):
        PENDING_CONFIRMATION = 'Pending Confirmation'
        CONFIRMED = 'Confirmed'
        CANCELLED = 'Cancelled'
        COMPLETED = 'Completed'

    # Define the Appointment model
    class Appointment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        date = db.Column(db.Date, nullable=False)
        time = db.Column(db.Time, nullable=False)

        # Define status options using Enum
        status = db.Column(db.Enum(AppointmentStatus), nullable=False, default=AppointmentStatus.PENDING_CONFIRMATION)

        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
        service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
        notes = db.Column(db.String(200), nullable=True)


    # Define methods
    # Init Method: Initializes Appointment object
    def __init__(self, date, time, user_id, business_id, service_id, notes):
        self.date = date
        self.time = time
        self.status = AppointmentStatus.PENDING_CONFIRMATION
        self.user_id = user_id
        self.business_id = business_id
        self.service_id = service_id
        self.notes = notes

    # Serialize Method: Converts object to dictionary for JSON serialization
    def serialize(self):
        return {
            'id': self.id,
            # Convert date to string if it is a date object and remove time information
            'date': self.date.strftime('%a, %d %b %Y') if self.date else None,
            # Convert time to string if it is a time object and remove milliseconds
            'time': self.time.strftime('%H:%M') if isinstance(self.time, time) else self.time,
            'status': self.status,
            'user_id': self.user_id,
            'business_id': self.business_id,
            'service_id': self.service_id,
            'notes': self.notes
        }
    
    # Get User Method: Returns the user associated with the appointment
    def get_user(self):
        return self.user.serialize()
            # Returns a dictionary representing the user associated with the appointment
    
    # Get Business Method: Returns the business associated with the appointment
    def get_business(self):
        return self.business.serialize()
            # Returns a dictionary representing the business associated with the appointment

    # Get Service Method: Returns the service associated with the appointment
    def get_service(self):
        return self.service.serialize()
            # Returns a dictionary representing the service associated with the appointment