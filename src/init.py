from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Create SQLAlchemy instance for importing globally into other modules
db = SQLAlchemy()
# Craete Marshmallow instance for importing globally into other modules
ma = Marshmallow()
# Craete Bcrypt instance for importing globally into other modules
bcrypt = Bcrypt()
# Craete JWT instance for importing globally into other modules
jwt = JWTManager()