from init import db
from flask import Blueprint
from models.game import Game
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
    games = [
        Game(
            title = 'God of War Ragnarok',
            year_released = '2022',
            genre = 'Action',
            platform = 'PS5',
            date_tracked = date.today(),
            status = 'Playing'
        ),
        Game(
            title = 'Red Dead Redemption 2',
            year_released = '2018',
            genre = 'Action',
            platform = 'PC',
            date_tracked = date.today(),
            status = 'Completed'
        ),
        Game(
            title = 'Bayonetta 3',
            year_released = '2022',
            genre = 'Action',
            platform = 'Switch',
            date_tracked = date.today(),
            status = 'Want to Play'
        )
    ]

    db.session.add_all(games)
    db.session.commit()
    print("Table seeded")