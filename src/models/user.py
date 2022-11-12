from init import db, ma
from marshmallow import fields
from marshmallow.validate import Length
# Create User model
class User(db.Model):
    # Define table name for Users model
    __tablename__ = 'users'

    # Define the attributes of the 'Users' table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default = False)

    # Define relationship with the Game model and the Note model
    # Cascade property reflects the one-to-many relationship, where if a user is deleted, all the related games and notes are deleted
    games = db.relationship('Game', back_populates = 'user', cascade = 'all, delete')
    notes = db.relationship('Note', back_populates = 'user', cascade = 'all, delete')

# Create schema to translate database objects into JSON readable objects
class UserSchema(ma.Schema):
    # Define how the games and notes fields are to be represented within the schema
    # Only include title and status for the games field
    # Exclude the user field for the notes fields 
    games = fields.List(fields.Nested('GameSchema', only = ['title', 'status']))
    notes = fields.List(fields.Nested('NoteSchema', exclude = ['user']))

    email = fields.Email()
    password = fields.String(required = True, validate= Length(min=1))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'date_joined', 'is_admin', 'games', 'notes')
        ordered = True