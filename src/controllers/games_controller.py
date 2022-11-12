from flask import Blueprint, request
from init import db
from models.game import Game, GameSchema
from models.note import Note, NoteSchema
from datetime import date
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import and_
from controllers.auth_controller import authorize

games_bp = Blueprint('games', __name__, url_prefix = '/games')

#================================================= GAMES =================================================

# GAME CONTROLLERS - GET, POST, PUT/PATCH, DELETE

# ~~~~~~~ READ: Retrieve information on all games ~~~~~~~

@games_bp.route('/')
def all_games():
    stmt = db.select(Game)
    games = db.session.scalars(stmt)
    return GameSchema(many=True).dump(games)

# ~~~~~~~ READ: Retrieve information for one game ~~~~~~~

@games_bp.route('/<int:game_id>/')
def one_game(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        return GameSchema().dump(game)
    else:
        return {'error': f'Game not found with id {game_id}'}, 404

# ~~~~~~~ CREATE: Add game to tracker ~~~~~~~

@games_bp.route('/', methods = ['POST'])
@jwt_required()
def add_game():
    data = GameSchema().load(request.json)
    game = Game(
        title = data['title'],
        year_released = data['year_released'],
        genre = data['genre'],
        platform = data['platform'],
        date_tracked = date.today(),
        status = data['status'],
        user_id = get_jwt_identity()
    )
    db.session.add(game)
    db.session.commit()
    return GameSchema().dump(game), 201

# ~~~~~~~ UPDATE: Update game details ~~~~~~~

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
        return {'error': f'Game not found with id {game_id}'}, 404

# ~~~~~~~ DELETE: Delete game from tracker ~~~~~~~

@games_bp.route('/<int:game_id>/', methods=['DELETE'])
@jwt_required()
def delete_one_card(game_id):
    stmt = db.select(Game).filter_by(id = game_id)
    game = db.session.scalar(stmt)
    if not game:
        return {'error': f'Game not found with id "{game_id}'}, 404
    if authorize() or game.user_id == get_jwt_identity:
        db.session.delete(game)
        db.session.commit()
        return {'message': f'Game "{game.title}" has been deleted successfully'}

#================================================= NOTES =================================================

# ~~~~~~~ READ: Retrieve all notes on a game ~~~~~~~

@games_bp.route('/<int:game_id>/notes/')
def all_notes_on_game(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if not game:
        return {'error': f'Game not found with id {game_id}'}, 404
    stmt = db.select(Note).filter_by(game_id=game_id)
    notes = db.session.scalars(stmt)
    if not notes:
        return {'message': f'No notes found under {game.title}'}
    return NoteSchema(many=True, exclude = ['game']).dump(notes)

# ~~~~~~~ READ: Retrieve one note ~~~~~~~

@games_bp.route('/notes/<int:note_id>/')
def get_one_note(note_id):
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    if note:
        return NoteSchema().dump(note)

# ~~~~~~~ CREATE: Add a note for a game ~~~~~~~

@games_bp.route('/<int:game_id>/notes/', methods = ['POST'])
@jwt_required()
def create_note(game_id):
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        data = NoteSchema().load(request.json)
        note = Note(
            description = data['description'],
            date = date.today(),
            tag = data['tag'],
            user_id = get_jwt_identity(),
            game = game
        )
        db.session.add(note)
        db.session.commit()
        return NoteSchema(exclude = ['game']).dump(note), 201
    else:
        return {'error': f'Game not found with id {game_id}'}, 404

# ~~~~~~~ UPDATE: Upate a note ~~~~~~~

@games_bp.route('/notes/<int:note_id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def edit_note(note_id):
    stmt = db.select(Note).where(and_(
        Note.id == note_id,
        Note.user_id == get_jwt_identity()
    ))
    note = db.session.scalar(stmt)
    if note:
        note.description = request.json.get('description') or note.description
        note.tag = request.json.get('tag') or note.tag
        db.session.commit()
        return NoteSchema().dump(note)
    else:
        return {'error': f'Note not found with id {note_id}'}

# ~~~~~~~ DELETE: Delete a note ~~~~~~~

@games_bp.route('/notes/<int:note_id>/', methods = ['DELETE'])
@jwt_required()
def delete_note(note_id):
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    if not note:
        return {'error': f'No comment found with id {note_id}'}
    if authorize() or note.user_id == get_jwt_identity:
        db.session.delete(note)
        db.session.commit()
        return 'This comment has been deleted.'

@games_bp.route('/test/')
@jwt_required()
def test():
    print(get_jwt_identity())
    return {}