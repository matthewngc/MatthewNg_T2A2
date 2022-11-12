from flask import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize
from init import db
from models.user import User

admin_bp = Blueprint('admin', __name__, url_prefix = '/admin')

@admin_bp.route('/<int:user_id>/give_admin/', methods = ['POST'])
@jwt_required()
def give_admin(user_id):
    authorize()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        if user.is_admin:
            return {'message': 'This user is already an admin!'}
        else:
            user.is_admin = True
            db.session.commit()
            return {'message': 'Success - you have given this user admin permissions.'}
    else:
        abort(404, description = f'User with id {user_id} does not exist!')

@admin_bp.route('/<int:user_id>/remove_admin/', methods = ['POST'])
@jwt_required()
def remove_admin(user_id):
    authorize()
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        if user.is_admin:
            user.is_admin = False
            db.session.commit()
            return {'message': 'Success - you have removed admin permissions from this user.'}
        else:
            return {'message': 'This user is not an admin!'}
    else:
        abort(404, description = f'User with id {user_id} does not exist!')