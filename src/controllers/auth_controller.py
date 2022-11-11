from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, UserSchema
from datetime import date
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, url_prefix = '/auth')

@auth_bp.route('/register/', methods=['POST'])
def auth_register():
    try:
        user = User(
            email = request.json.get('email'),
            password = bcrypt.generate_password_hash(request.json.get('password')).decode('utf-8'),
            name = request.json.get('name'),
            date_joined = date.today()
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    except IntegrityError:
        return {'error': 'Email address already in use'}, 409

@auth_bp.route('/login/', method = ['POST'])
def auth_login():
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        t