from init import db, ma

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    year_released = db.Column(db.String)
    genre = db.Column(db.String)
    platform = db.Column(db.String)
    date_tracked = db.Column(db.Date)
    status = db.Column(db.String)

class GameSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'year_released', 'genre', 'platform', 'date_tracked', 'status')
        ordered = True