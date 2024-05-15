# Appointment Model

# Import dependencies
from server.database import db
from datetime import time


# Define model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        # User ID is a foreign key to the User model
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
        # Business ID is a foreign key to the Business model
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
        # Service ID is a foreign key to the Service model
    notes = db.Column(db.String(200), nullable=True)


    # Define methods
    # Init Method: Initializes Appointment object
    def __init__(self, date, time, user_id, business_id, service_id, notes):
        self.date = date
        self.time = time
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