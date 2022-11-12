from init import db, ma 
from marshmallow import fields
from marshmallow.validate import OneOf, Length

# Assign list of valid tags for validation
VALID_TAGS = ('Review', 'Comment', 'Reminder', 'Progress', 'Tips', 'Request')

# Create Note model
class Note(db.Model):
    # Define table name for Note model
    __tablename__ = 'notes'

    # Define the attributes of the 'Notes' table
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(1000), nullable=False)
    date = db.Column(db.Date)
    tag = db.Column(db.String, default = VALID_TAGS[1])

    # Defining the foreign keys relating to the User and Game model
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)


    # Define relationship with the User model and the Game model
    user = db.relationship('User', back_populates='notes')
    game = db.relationship('Game', back_populates='notes')

# Create schema to translate database objects into JSON readable objects
class NoteSchema(ma.Schema):
    # Define how the user and games fields are to be represented within the schema
    # Only include name and email in the user fields
    user = fields.Nested('UserSchema', only = ['name', 'email'])
    game = fields.Nested('GameSchema', only = ['title', 'status'])

    # Validation of description and tag fields
    # Description must be at least 1 character long
    description = fields.String(required=True, validate=Length(min=1))
    # Tag must be a string that is listed within VALID_TAGS
    tag = fields.String(validate=OneOf(VALID_TAGS), error=f'Status must be one of the following: {VALID_TAGS}')

    class Meta:
        fields = ('id', 'description', 'date', 'tag', 'game', 'user')
        ordered = True