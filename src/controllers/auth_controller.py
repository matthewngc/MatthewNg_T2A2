from flask import Blueprint, request, abort
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

#================================================= AUTHENTICATION =================================================

# ~~~~~~~ Register a new user ~~~~~~~

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        # Load JSON data into schema for validation
        data = UserSchema().load(request.json)
        # Add user data where provided
        user = User(
            email = data['email'],
            password = bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            name = data['name'],
            date_joined = date.today()
        )
        # Add and commit to database
        db.session.add(user)
        db.session.commit()
        # Return confirmation message and show user data
        return {'message': 'You are now registered!',
                'user': UserSchema(exclude=['password']).dump(user)}, 201
    # Show error message if email provide is in use 
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

# ~~~~~~~ Login a registered user ~~~~~~~

@auth_bp.route('/login/', methods=['POST'])
def auth_login():
    # Select query to retrieve user with provided email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # Check that the user exists and the password matches the database
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        # Create JWT token for user
        token = create_access_token(identity = str(user.id), expires_delta = timedelta(days=1))
        # Return confirmation message, token, email and admin privileges
        return {'message': 'You have successfully logged in!',
                'email': user.email, 
                'token': token, 
                'is_admin': user.is_admin}
    # Return error message if email or password do not match
    else:
        return {'error': 'Invalid email or password - please try again.'}, 401

# ~~~~~~~ Authorisation Function ~~~~~~~
# Authorisation function to verify admin privileges
def authorize():
    # Select query to retrieve user with the provided JWT token
    stmt = db.select(User).filter_by(id = get_jwt_identity())
    user = db.session.scalar(stmt)
    # If the user is not an admin, abort and return error message
    if not user.is_admin:
        abort(401)
    return True