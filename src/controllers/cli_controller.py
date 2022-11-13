from init import db, bcrypt
from flask import Blueprint
from models.game import Game
from models.user import User
from models.note import Note
from datetime import date

db_commands = Blueprint('db', __name__)

#================================================= CUSTOM CLI COMMANDS =================================================

# CLI command to create tables as per the User, Game and Note models in the database
@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

# CLI command to drop all existing tables in the database
@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

# CLI command to seed the created tables with records for testing purposes
@db_commands.cli.command('seed')
def seed_db():
    # Create list of User classes with fields to be seeded into the User table
    users = [
        User(
            email = 'admin@gametracker.com',
            password = bcrypt.generate_password_hash('admin123').decode('utf-8'),
            is_admin = True
        ),
        User(
            name = 'Timothy Newman',
            email = 'timmynewman@abc.com',
            password = bcrypt.generate_password_hash('bballxyz').decode('utf-8'),
            date_joined = '10/10/2020'
        ),
        User(
            name = 'Anthony Quinn',
            email = 'antoquinn@abc.com',
            password = bcrypt.generate_password_hash('password').decode('utf-8'),
            date_joined = '5/23/2021'
        )
    ]

    # Add user instances to the database and commit changes
    db.session.add_all(users)
    db.session.commit()

    # Create list of Game classes with fields to be seeded into the Game table
    games = [
        Game(
            title = 'God of War Ragnarok',
            year_released = '2022',
            genre = 'Action',
            platform = 'PS5',
            date_tracked = date.today(),
            status = 'Playing',
            user_id = users[2].id
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
            user_id = users[2].id
        )
    ]

    # Add game instances to the database and commit changes
    db.session.add_all(games)
    db.session.commit()

    # Create list of Note classes with fields to be seeded into the Note table
    notes = [
        Note(
            description = 'This is a good game',
            tag = 'Review',
            user = users[1],
            game = games[1],
            date = date.today(),
        ),
        Note(
            description = 'Up to second bossfight',
            tag = 'Progress',
            user = users[2],
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

    # Add note instances to the database and commit changes
    db.session.add_all(notes)
    db.session.commit()
    print("Table seeded")

