from init import db, ma
from marshmallow import fields

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_joined = db.Column(db.Date)
    is_admin = db.Column(db.Boolean, default = False)

    games = db.relationship('Game', back_populates = 'user', cascade = 'all, delete')
    notes = db.relationship('Note', back_populates = 'user', cascade = 'all, delete')

class UserSchema(ma.Schema):
    games = fields.List(fields.Nested('GameSchema', exclude = ['user']))
    notes = fields.List(fields.Nested('NoteSchema', exclude = ['user']))

    class Meta:
        fields = ('id', 'name', 'email', 'password', 'date_joined', 'is_admin', 'games', 'notes')
        ordered = True