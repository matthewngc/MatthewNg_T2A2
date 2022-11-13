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
# No authentication required
@games_bp.route('/')
def all_games():
    # Select query to retrieve all games tracked in the database
    stmt = db.select(Game)
    games = db.session.scalars(stmt)

    return GameSchema(many=True).dump(games)

# ~~~~~~~ READ: Retrieve information for one game ~~~~~~~
# No authentication required
@games_bp.route('/<int:game_id>/')
def one_game(game_id):
    # Select query to retrieve one game from database filtered by the game id
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    # Check if game id exists - return 404 if it does not
    if game:
        return GameSchema().dump(game)
    else:
        return {'error': f'Game not found with id {game_id}'}, 404

# ~~~~~~~ CREATE: Add game to tracker ~~~~~~~
# Authentication required - users must be logged in to add games to tracker
@games_bp.route('/', methods = ['POST'])
# Request JWT token
@jwt_required()
def add_game():
    # Load JSON data into schema for validation
    data = GameSchema().load(request.json)
    # Create new game object based on fields from request
    game = Game(
        title = data['title'],
        year_released = data['year_released'],
        genre = data['genre'],
        platform = data['platform'],
        date_tracked = date.today(),
        status = data['status'],
        user_id = get_jwt_identity()
    )

    # Add to database and commit
    db.session.add(game)
    db.session.commit()

    # Return confirmation message and data of game added
    return {'message': f'You are now tracking {game.title}!',
            'game': GameSchema().dump(game)}, 201

# ~~~~~~~ UPDATE: Update game details ~~~~~~~
# Authentication required - users must be logged in to update their games
# Admins can also update games on any user's profile
@games_bp.route('/<int:game_id>/', methods = ['PUT', 'PATCH'])
# Request JWT token
@jwt_required()
def update_game(game_id):
    # Select query to retrieve game with the given game id from database
    stmt = db.select(Game).filter_by(id = game_id)
    game = db.session.scalar(stmt)
    # If the game with this id does not exist, return error message
    if not game:
        return {'error': f'Game not found with id {game_id}'}, 404
    # Check that the user making the change is the owner of the game OR an admin is making a change
    if game.user_id == int(get_jwt_identity()) or authorize():
        # Load JSON data into schema for validation
        data = GameSchema().load(request.json, partial = True)
        # Update fields where provided
        if request.json.get('title'):
            game.title = data['title']
        if request.json.get('year_released'):
            game.year_released = data['year_released']
        if request.json.get('genre'):
            game.genre = data['genre']
        if request.json.get('platform'):
            game.platform = data['platform']
        if request.json.get('status'):
            game.status = data['status']
        # Commit changes to the database
        db.session.commit()
        # Show confirmation message and updated game data
        return {'message': f'You have updated the details of {game.title}!',
                'game': GameSchema().dump(game)
        }


# ~~~~~~~ DELETE: Delete game from tracker ~~~~~~~
# Authentication required - users can only delete their own games or need admin privileges
@games_bp.route('/<int:game_id>/', methods=['DELETE'])
# Request JWT token
@jwt_required()
def delete_one_game(game_id):
    # Select query to retrieve game with game_id from database
    stmt = db.select(Game).filter_by(id = game_id)
    game = db.session.scalar(stmt)
    # If the game with the game id does not exist, return error message
    if not game:
        return {'error': f'Game not found with id "{game_id}'}, 404
    # Check that the user deleting the game is the owner of the game OR an admin is deleting
    if game.user_id == int(get_jwt_identity()) or authorize():
        db.session.delete(game)
        db.session.commit()
        return {'message': f'Game "{game.title}" has been deleted successfully'}

#================================================= NOTES =================================================

# ~~~~~~~ READ: Retrieve all notes on a game ~~~~~~~
# No authentication required
@games_bp.route('/<int:game_id>/notes/')
def all_notes_on_game(game_id):
    # Select query to retrieve game with game_id from database
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    # If the game with the game id does not exist, return error message
    if not game:
        return {'error': f'Game not found with id {game_id}'}, 404
    # Select query to retrieve all notes with this game id
    stmt = db.select(Note).filter_by(game_id=game_id)
    notes = db.session.scalars(stmt)
    # If no notes exist under this game id, return error message
    if not notes:
        return {'message': f'No notes found under {game.title}'}, 404
    # Return all notes under this game id
    return NoteSchema(many=True, exclude = ['game']).dump(notes)

# ~~~~~~~ READ: Retrieve one note ~~~~~~~
# No authentication required
@games_bp.route('/notes/<int:note_id>/')
def get_one_note(note_id):
    # Select query to retrieve note with this note id
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    # If the note does not exist, return error message
    if not note:
        return {'error': f'Note not found with id {note_id}'}, 404
    # Otherwise return the note with this note id
    else:
        return NoteSchema().dump(note)

# ~~~~~~~ CREATE: Add a note for a game ~~~~~~~
# Authentication required - users must be logged in to create a note
@games_bp.route('/<int:game_id>/notes/', methods = ['POST'])
# Request JWT token
@jwt_required()
def create_note(game_id):
    # Select query to retrieve game with game_id from database
    stmt = db.select(Game).filter_by(id=game_id)
    game = db.session.scalar(stmt)
    if game:
        # Load JSON data into schema for validation
        data = NoteSchema().load(request.json)
        # Create new note object based on fields from request
        note = Note(
            description = data['description'],
            date = date.today(),
            tag = data['tag'],
            user_id = get_jwt_identity(),
            game = game
        )
        # Add to database and commit
        db.session.add(note)
        db.session.commit()
        # Return confirmation message and note data
        return {'message': f'You have created a note for {game.title}',
                'note': NoteSchema(exclude = ['game']).dump(note)}, 201
    # If no game found with the provided game id, return error message
    else:
        return {'error': f'Game not found with id {game_id}'}, 404

# ~~~~~~~ UPDATE: Upate a note ~~~~~~~
# Authentication required - users can only update the notes they have posted, or have admin rights
@games_bp.route('/notes/<int:note_id>', methods = ['PUT', 'PATCH'])
@jwt_required()
def edit_note(note_id):
    # Select query to retrive the note with the given note id from database
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    # if the note with this id does not exist, return error message
    if not note:
        return {'error': f'Note not found with id {note_id}'}, 404
    # Check that the user making the change is the owner of the note or an admin
    if note.user_id == int(get_jwt_identity()) or authorize():
        # Load JSON data into schema for validation
        data = NoteSchema().load(request.json)
        # Update fields where provided
        if request.json.get('description'):
            note.description = data['description']
        if request.json.get('tag'):
            note.tag = data['tag']
        # Commit changes
        db.session.commit()
        # Return confirmation message and note data
        return {'message': f'You have updated note with id {note.id}!',
                'note': NoteSchema().dump(note)}

# ~~~~~~~ DELETE: Delete a note ~~~~~~~
# Authentication required - users can only delete their own notes or need admin rights
@games_bp.route('/notes/<int:note_id>/', methods = ['DELETE'])
# Request JWT token
@jwt_required()
def delete_note(note_id):
    # Select query to retrieve note with give note id from database
    stmt = db.select(Note).filter_by(id = note_id)
    note = db.session.scalar(stmt)
    # If the note with this id does not exist, return error message
    if not note:
        return {'error': f'No note found with id {note_id}'}, 404
    # Check that the user making the change is the owner of the note or an admin    
    if note.user_id == int(get_jwt_identity()) or authorize():
        db.session.delete(note)
        db.session.commit()
        return {'message': 'This note has been deleted.'}

