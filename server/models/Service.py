# Service Model


# Import dependencies
from server.database import db


# Define model
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True) 
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
        # Business ID is a foreign key to the Business model
    appointments = db.relationship('Appointment', backref='service', lazy=True)
        # Appointments is a list of Appointment objects associated with the Service
            # backref='service' creates a service attribute in the Appointment model
            # lazy=True means data is loaded as necessary

    # Define methods
    # Init Method: Initializes Service object
    def __init__(self, name, duration, price, description, business_id): 
        self.name = name
        self.duration = duration
        self.price = price
        self.description = description
        self.business_id = business_id

    # Serialize Method: Converts object to dictionary for JSON serialization
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'duration': self.duration,
            'price': self.price,
            'description': self.description 
        }
    
    # Get Appointments Method: Returns a list of appointments associated with the service
    def get_appointments(self):
        return [appointment.serialize() for appointment in self.appointments]
            # Returns a list of dictionaries representing the appointments associated with the service    
    


        
    

