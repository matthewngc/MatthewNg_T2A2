from flask import Blueprint, request
from init import db
from models.game import Game, GameSchema
from models.note import Note, NoteSchema
from datetime import date

games_bp = Blueprint('games', __name__, url_prefix = '/games')

@games_bp.route('/')
def all_games():
    stmt = db.select(Game)
    games = db.session.scalars(stmt)
    return GameSchema(many=True).dump(games)

@games_bp.route('/<int:game_id>')
def one_game(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        return GameSchema().dump(game)
    else:
        return {'error': f'Game not found with id {game_id}'}, 404

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

@games_bp.route('/<int:game_id>/', methods = ['PUT', 'PATCH'])
def update_one_game(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        game.title = request.json.get('title') or game.title
        game.year_released = request.json.get('year_released') or game.year_released
        game.genre = request.json.get('genre') or game.genre
        game.platform = request.json.get('platform') or game.platform
        game.status = request.json.get('status') or game.status
        db.session.commit()
        return GameSchema().dump(game)
    else:
        return {'error': f'Card not found with id {game_id}'}, 404

@games_bp.route('/<int:game_id>/', methods=['DELETE'])
def delete_one_card(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        db.session.delete(game)
        db.session.commit()
        return {'message': f'Game "{game.title}" has been deleted successfully'}
    else:
        return {'error': f'Game not found with id "{game_id}'}, 404

@games_bp.route('/<int:game_id>/notes/')
def all_notes_on_game(game_id):
    stmt = db.select(Note).filter_by(id=game_id)
    notes = db.session.scalars(stmt)
    if notes:
        return NoteSchema(many=True, exclude = ['game']).dump(notes)

@games_bp.route('/notes/<int:note_id>/')
def get_one_note(note_id):
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    if note:
        return NoteSchema().dump(note)

