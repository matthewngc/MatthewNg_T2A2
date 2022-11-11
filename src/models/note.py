from init import db, ma 

class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    tag = db.Column(db.String)

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'description', 'date', 'tag')
        ordered = True