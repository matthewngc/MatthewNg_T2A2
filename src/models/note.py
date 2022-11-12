from init import db, ma 
from marshmallow import fields

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    tag = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable = False)

    user = db.relationship('User', back_populates='notes')
    game = db.relationship('Game', back_populates='notes')

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'date', 'tag', 'game', 'user')
        ordered = True