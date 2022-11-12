from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required

users_bp = Blueprint('users',__name__, url_prefix='/users')

#================================================= USERS =================================================


@users_bp.route('/profile/')
@jwt_required()
def get_user():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    if user:
        return UserSchema(exclude=['password']).dump(user)

@users_bp.route('/profile/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_profile():
    stmt = db.select(User).filter_by(id=get_jwt_identity())
    user = db.session.scalar(stmt)
    if user:
        user.name = request.json.get('name') or user.name
        user.email = request.json.get('email') or user.email
        if request.json.get('password'):
            user.password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8') or user.password
        db.session.commit()

        return {
            'message': 'You have updated your details!',
            'user': UserSchema(exclude=['password']).dump(user)
        }

