from flask import Blueprint
from init import db
from models.game import Game, GameSchema
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix = '/games')

@games_bp.route('/')
def all_games():
    stmt = db.select(Game)
    games = db.session.scalars(stmt)
    return GameSchema(many=True).dump(games)