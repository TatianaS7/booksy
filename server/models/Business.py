# Business Model 


# Import dependencies
from server import db
from bcrypt import hashpw, gensalt, checkpw


# Define model
class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # Services is a list of Service objects associated with the Business
    services = db.relationship('Service', backref='business', lazy=True)
        # backref='business' creates a business attribute in the Service model
        # lazy=True means data is loaded as necessary

    # Appointments is a list of Appointment objects associated with the Business
    appointments = db.relationship('Appointment', backref='business', lazy=True)
        # backref='business' creates a business attribute in the Appointment model
        # lazy=True means data is loaded as necessary

    # Define methods
    # Init Method: Initializes Business object
    def __init__(self, name, address, city, state, phone_number, email, password):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.phone_number = phone_number
        self.email = email
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            # hashpw() hashes the password using bcrypt and gensalt() generates a salt value

    # Serialize Method: Converts object to dictionary for JSON serialization
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'phone_number': self.phone_number,
            'email': self.email,

            # Services is a list of dictionaries
            'services': [service.serialize() for service in self.services],

            # Appointments is a list of dictionaries
            'appointments': [appointment.serialize() for appointment in self.appointments]
        }
    
    # Check Password Method: Checks if the password is correct
    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
            # checkpw() compares the hashed password with the plaintext password