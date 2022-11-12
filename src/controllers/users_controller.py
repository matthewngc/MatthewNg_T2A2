from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

users_bp = Blueprint('users',__name__, url_prefix='/users')

#================================================= USERS =================================================

# ~~~~~~~ Read user profile ~~~~~~~
# Authentication required - users must be logged in to view their own profile
@users_bp.route('/profile/')
# Request JWT token
@jwt_required()
def get_profile():
    # Select query to retrieve user with this token from the database
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # Return user profile data
    return UserSchema(exclude=['password']).dump(user)

# ~~~~~~~ Update user profile ~~~~~~~
# Authentication required - users must be logged in to update their profile
@users_bp.route('/profile/', methods=['PUT', 'PATCH'])
# Request JWT token
@jwt_required()
def update_profile():
    # Select query to retrieve user with this token from the database
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    # Load JSON data into schema for validation
    data = UserSchema().load(request.json)
    # Update fields where provided
    if request.json.get('name'):
        user.name = data['name']
    if request.json.get('email'):
        user.email = data['email']
    if request.json.get('password'):
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    # Commit changes
    db.session.commit()
    # Return confirmation message and show user data
    return {
        'message': 'You have updated your details!',
        'user': UserSchema(exclude=['password']).dump(user)
    }

