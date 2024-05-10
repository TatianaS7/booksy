# User Model


# Import dependencies
from server.database import db
from bcrypt import hashpw, gensalt, checkpw


# Define model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
   
    # Appointments is a list of Appointment objects associated with the User
    appointments = db.relationship('Appointment', backref='user', lazy=True)
        # backref='user' creates a user attribute in the Appointment model
        # lazy=True means data is loaded as necessary


# Define methods
# Init Method: Initializes User object
    def __init__(self, full_name, email, username, phone_number, password):
        self.full_name = full_name
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')
            # hashpw() hashes the password using bcrypt and gensalt() generates a salt value

# Serialize Method: Converts object to dictionary for JSON serialization
    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'username': self.username,
            'phone_number': self.phone_number,

            # Appointments is a list of dictionaries
            'appointments': [appointment.serialize() for appointment in self.appointments]
        }
    
# Check Password Method: Checks if the password is correct
    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
            # checkpw() compares the hashed password with the plaintext password


    