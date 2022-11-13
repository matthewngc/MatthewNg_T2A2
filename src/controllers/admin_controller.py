from flask import Blueprint, abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.auth_controller import authorize
from init import db, bcrypt
from models.user import User, UserSchema

admin_bp = Blueprint('admin', __name__, url_prefix = '/admin')

#================================================= ADMINS =================================================
# ~~~~~~~ Give admin permissions to a user ~~~~~~~

# Authentication required - only admins can give admin permissions
@admin_bp.route('/<int:user_id>/give_admin/', methods = ['POST'])
# Request JWT token
@jwt_required()
def give_admin(user_id):
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve user with the given user id from database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Check that the user exists in the database
    if user:
        # Return message if the user is already an admin
        if user.is_admin:
            return {'message': 'This user is already an admin!'}
        # Set is.admin attribute to True, commit changes and return confirmation message
        else:
            user.is_admin = True
            db.session.commit()
            return {'message': 'Success - you have given this user admin permissions.'}
    # If user is not found with this user id, return error message
    else:
        abort(404, description = f'User with id {user_id} does not exist!')

# ~~~~~~~ Remove admin permissions from a user ~~~~~~~

# Authentication required - only admins can remove admin permissions
@admin_bp.route('/<int:user_id>/remove_admin/', methods = ['POST'])
# Request JWT token
@jwt_required()
def remove_admin(user_id):
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve user with the given user id from database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    # Check that the user exists in the database
    if user:
        # Set is.admin attribute to False, commit changes and return confirmation message
        if user.is_admin:
            user.is_admin = False
            db.session.commit()
            return {'message': 'Success - you have removed admin permissions from this user.'}
        # Return message if the user is not an admin
        else:
            return {'message': 'This user is not an admin!'}
    # If user is not found with this user id, return error message
    else:
        abort(404, description = f'User with id {user_id} does not exist!')

# ~~~~~~~ READ: retrieve all registered users ~~~~~~~

@admin_bp.route('/all_users/')
# Request JWT token
@jwt_required()
def all_users():
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve all users in the database
    stmt = db.select(User)
    users = db.session.scalars(stmt)
    # Return all registered user data
    return UserSchema(many=True, exclude = ['password']).dump(users)

# ~~~~~~~ READ: retrieve one registered user ~~~~~~~

@admin_bp.route('/user/<int:user_id>')
# Request JWT token
@jwt_required()
def one_user(user_id):
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve user with the provided user id in the database
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    # If the user exists, return user data
    if user:
        return UserSchema(exclude = ['password']).dump(user)
    # If the user does not exist, return error message
    else:
        abort(404, description = f'User with id {user_id} does not exist!')

# ~~~~~~~ PUT/PATCH: update a user's details ~~~~~~~

@admin_bp.route('/user/<int:user_id>', methods=['PUT', 'PATCH'])
# Request JWT token
@jwt_required()
def update_user(user_id):
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve user with the provided user id in the database
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        # Load JSON data into schema for validation
        data = UserSchema().load(request.json)
        # Update fields where provided
        if request.json.get('name'):
            user.name = data['name']
        if request.json.get('email'):
            user.email = data['email']
        if request.json.get('password'):
            user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        # Commit changes to database
        db.session.commit()
        # Return confirmation message and user data
        return {
            'message': "You have updated this user's details!",
            'user': UserSchema(exclude=['password']).dump(user)
        }
    # If the user with this user id does not exist, return error message
    else:
        abort(404, description = f'User with id {user_id} does not exist!')        

# ~~~~~~~ Delete a registered user ~~~~~~~

# Authentication required - only admins can delete users
@admin_bp.route('user/<int:user_id>', methods = ['DELETE'])
# Request JWT token
@jwt_required()
def delete_user(user_id):
    # Check that the logged in user is an admin
    authorize()
    # Select query to retrieve user with the provided user id in the database
    stmt = db.select(User).filter_by(id = user_id)
    user = db.session.scalar(stmt)
    if user:
        # Delete user and commit to database
        db.session.delete(user)
        db.session.commit()
        # Return confirmation message and deleted user details
        return {
            'message': 'You have successfully deleted this user.',
            'user_id': user_id,
            'name': user.name,
            'email': user.email
        }
    # If user with user id not found, return error message
    else:
        abort(404, description = f'User with id {user_id} does not exist!')
