from init import db, bcrypt
from flask import Blueprint
from models.game import Game
from models.user import User
from models.note import Note
from datetime import date

db_commands = Blueprint('db', __name__)

@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email = 'admin@gametracker.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Cameron Johnson',
            email = 'camjohnson@abc.com',
            password = bcrypt.generate_password_hash('bballxyz').decode('utf-8'),
            date_joined = '10/10/2020'
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    games = [
        Game(
            title = 'God of War Ragnarok',
            year_released = '2022',
            genre = 'Action',
            platform = 'PS5',
            date_tracked = date.today(),
            status = 'Playing',
            user_id = users[0].id
        ),
        Game(
            title = 'Red Dead Redemption 2',
            year_released = '2018',
            genre = 'Action',
            platform = 'PC',
            date_tracked = date.today(),
            status = 'Completed',
            user_id = users[1].id
        ),
        Game(
            title = 'Bayonetta 3',
            year_released = '2022',
            genre = 'Action',
            platform = 'Switch',
            date_tracked = date.today(),
            status = 'Want to Play',
            user_id = users[0].id
        )
    ]


    db.session.add_all(games)
    db.session.commit()

    notes = [
        Note(
            description = 'This is a good game',
            tag = 'Review',
            user = users[0],
            game = games[1],
            date = date.today(),
        ),
        Note(
            description = 'Up to second bossfight',
            tag = 'Progress',
            user = users[1],
            game = games[0],
            date = date.today()
        ),
        Note(
            description = 'On sale at JB HiFI this week',
            tag = 'Comment',
            user = users[1],
            game = games[2],
            date = date.today()
        )
    ]

    db.session.add_all(notes)
    db.session.commit()
    print("Table seeded")

