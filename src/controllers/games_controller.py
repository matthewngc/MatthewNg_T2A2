from flask import Blueprint, request
from init import db
from models.game import Game, GameSchema
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix = '/games')

@games_bp.route('/')
def all_games():
    stmt = db.select(Game)
    games = db.session.scalars(stmt)
    return GameSchema(many=True).dump(games)

@games_bp.route('/<int:id>')
def one_game(id):
    stmt = db.select(Game).filter_by(id=id)
    game = db.session.scalar(stmt)
    if game:
        return GameSchema().dump(game)
    else:
        return {'error': f'Game not found with id {id}'}, 404

@games_bp.route('/', methods = ['POST'])
def add_game():
    game = Game(
        title = request.json['title'],
        year_released = request.json['year_released'],
        genre = request.json['genre'],
        platform = request.json['platform'],
        date_tracked = date.today(),
        status = request.json['status']
    )
    db.session.add(game)
    db.session.commit()
    return GameSchema().dump(game), 201