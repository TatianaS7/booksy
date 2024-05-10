# Import db and ma from the app module
from app import db, ma


# Import the Routes
from .routes import user

# Import the Models
from server.models import User, Business, Appointment, Service
