from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.cli_controller import db_commands
from controllers.games_controller import games_bp
from controllers.auth_controller import auth_bp
from controllers.users_controller import users_bp
import os

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(games_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(users_bp)

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You do not have the appropriate permissions to perform this action.'}, 401

    return app

