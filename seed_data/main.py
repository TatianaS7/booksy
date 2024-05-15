# Write function to seed data from JSON files in server/seed_data
from datetime import time, datetime
from server.models import User, Appointment, Service, Business
import json
import bcrypt
from server.database import db

def seedData():
    try:
        # Clear all tables
        db.session.query(User).delete()
        db.session.query(Appointment).delete()
        db.session.query(Service).delete()
        db.session.query(Business).delete()

        # Open User JSON file
        with open('seed_data/seedUsers.json') as f:
            users = json.load(f)
            for user in users:
                hashed = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
                new_user = User(
                    full_name=user['full_name'],
                    email=user['email'],
                    username=user['username'],
                    phone_number=user['phone_number'],
                    password=hashed.decode('utf-8')
                )
                db.session.add(new_user)
            db.session.commit()
        
        # Open Business JSON file
        with open('seed_data/seedBusinesses.json') as f:
            businesses = json.load(f)
            for business in businesses:
                new_business = Business(
                    name=business['name'],
                    address=business['address'],
                    city=business['city'],
                    state=business['state'],
                    phone_number=business['phone_number'],
                    email=business['email'],
                    password=business['password'],
                )
                db.session.add(new_business)
            db.session.commit()

        # Open Service JSON file
        with open('seed_data/seedServices.json') as f:
            services = json.load(f)
            for service in services:
                new_service = Service(
                    name=service['name'],
                    duration=service['duration'],
                    price=service['price'],
                    description=service['description'],
                    business_id=service['business_id'],
                )
                db.session.add(new_service)
            db.session.commit()
        
        # Open Appointment JSON file
        with open('seed_data/seedAppointments.json') as f:
            appointments = json.load(f)
            for appointment in appointments:
                # Convert date string to date object - Python objects are not JSON serializable
                date_str = appointment['date']
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                appointment['date'] = date_obj

                # Convert time string to time object - Python objects are not JSON serializable
                time_str = appointment['time']
                # Remove milliseconds from time string
                time_obj = datetime.strptime(time_str[:-3], '%H:%M').time()
                appointment['time'] = time_obj

                new_appointment = Appointment(
                    date=appointment['date'],
                    time=appointment['time'],
                    user_id=appointment['user_id'],
                    business_id=appointment['business_id'],
                    service_id=appointment['service_id'],
                    notes=appointment['notes']
                )
                db.session.add(new_appointment)
            db.session.commit()
        
        print('Data Seeded Successfully!')
    
    except Exception as e:
        print(f'Error occurred while seeding data: {str(e)}')

