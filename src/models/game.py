from init import db, ma
from marshmallow import fields

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year_released = db.Column(db.String)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    date_tracked = db.Column(db.Date)
    status = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    
    user = db.relationship('User', back_populates='games')
    notes = db.relationship('Note', back_populates='game', cascade = 'all, delete')

class GameSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=['name', 'email'])
    notes = fields.List(fields.Nested('NoteSchema', exclude = ['game']))
    class Meta:
        fields = ('id', 'title', 'year_released', 'genre', 'platform', 'date_tracked', 'status', 'user', 'notes')
        ordered = True