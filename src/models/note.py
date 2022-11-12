from init import db, ma 
from marshmallow import fields
from marshmallow.validate import OneOf, Length

VALID_TAGS = ('Review', 'Comment', 'Reminder', 'Progress', 'Tips', 'Request')

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date)
    tag = db.Column(db.String, default = VALID_TAGS[1])

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)

    user = db.relationship('User', back_populates='notes')
    game = db.relationship('Game', back_populates='notes')

class NoteSchema(ma.Schema):
    description = fields.String(required=True, validate=Length(min=1))
    tag = fields.String(validate=OneOf(VALID_TAGS), error=f'Status must be one of the following: {VALID_TAGS}')
    user = fields.Nested('UserSchema', only = ['name', 'email'])
    game = fields.Nested('GameSchema')

    class Meta:
        fields = ('id', 'description', 'date', 'tag', 'game', 'user')
        ordered = True