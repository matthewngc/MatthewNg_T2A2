from init import db, ma
from marshmallow import fields
from marshmallow.validate import OneOf, Length

# Assign list of valid statuses for validation
VALID_STATUSES = ('Currently Playing', 'Completed', 'Dropped', 'On Hold', 'Want To Play')

# Create Game model
class Game(db.Model):
    # Define table name for games model
    __tablename__ = 'games'

    # Define the attributes of the 'Games' table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    year_released = db.Column(db.String)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    date_tracked = db.Column(db.Date)
    status = db.Column(db.String)

    # Defining the foreign key relating to the User model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    # Define relationship with the User model and the Note model
    # Cascade property reflects the one-to-many relationship, where if a game is deleted, all the related notes are deleted
    user = db.relationship('User', back_populates='games')
    notes = db.relationship('Note', back_populates='game', cascade = 'all, delete')

# Create schema to translate database objects into JSON readable objects
class GameSchema(ma.Schema):
    # Define how the user and notes fields are to be represented within the schema
    # Only include name and email in the user fields
    user = fields.Nested('UserSchema', only=['name', 'email'])
    # Exclude game from the notes field
    notes = fields.List(fields.Nested('NoteSchema', exclude = ['game']))

    # Validation of title and status fields
    # Title must be at least 1 character long
    title = fields.String(validate = Length(min=1))
    # Status must be a string that is listed within VALID_STATUSES
    status = fields.String(validate= OneOf(VALID_STATUSES, error=f'Status must be one of the following: {VALID_STATUSES}'))

    class Meta:
        fields = ('id', 'title', 'year_released', 'genre', 'platform', 'date_tracked', 'status', 'user', 'notes')
        ordered = True