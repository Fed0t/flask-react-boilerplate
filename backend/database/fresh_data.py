from flask_security.utils import encrypt_password
from database.user import db, user_datastore

#############################################
########## Bootstrap Several Users
#############################################

def create_models():
    # Create the default roles
    reseller = user_datastore.find_or_create_role(name='reseller', description="Reseller basic user")
    seller = user_datastore.find_or_create_role(name='seller', description="Seller basic user")
    manufacturer = user_datastore.find_or_create_role(name='manufacturer', description="Manufacturer basic user")
    admin = user_datastore.find_or_create_role(name='admin', description='API Administrator')

    # Create the default users
    user_datastore.create_user(email='serghei@veelancing.io', password=encrypt_password('testing123'), first_name="Serghei", last_name=" Test User")
    user_datastore.create_user(email='ionut@veelancing.io', password=encrypt_password('testing123'), first_name="Ionut", last_name="Test User")
    user_datastore.create_user(email='stefan@veelancing.io', password=encrypt_password('testing123'), first_name="Vanea", last_name="Test User")
    user_datastore.create_user(email='bobe@veelancing.io', password=encrypt_password('testing123'), first_name="Bobe", last_name="Test User")

    # Save users
    db.session.commit()

    # Activate users and assign roles
    user1 = user_datastore.find_user(email='serghei@veelancing.io')
    user2 = user_datastore.find_user(email='ionut@veelancing.io')
    user3 = user_datastore.find_user(email='stefan@veelancing.io')
    user4 = user_datastore.find_user(email='bobe@veelancing.io')

    user_datastore.activate_user(user1) 
    user_datastore.activate_user(user2)
    user_datastore.activate_user(user3)
    user_datastore.activate_user(user4)

    user_datastore.add_role_to_user(user1, admin)
    user_datastore.add_role_to_user(user2, seller)
    user_datastore.add_role_to_user(user3, manufacturer)
    user_datastore.add_role_to_user(user4, reseller)

    # Save changes
    db.session.commit()