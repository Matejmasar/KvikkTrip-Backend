from app import app
from flask import jsonify, request
from app.services.users import Users

'''
 CRUD API for Users table
'''
@app.route('/users', methods=['GET'])
def get_all_usernames():
    all_users = Users.query.all()
    if all_users is None or len(all_users) == 0:
        return "There are no users in the database"
    else:
        return jsonify([user.serialize() for user in all_users]), 200

@app.route('/user/<int:user_id>', methods=['GET'])
def user_get(user_id):
    user = Users.get_user_by_id(user_id)
    if user:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user', methods=['POST'])
def user_post():
    data = request.json
    username = data.get('name')
    email = data.get('email')

    if not username: 
        return jsonify({'error': 'Missing User Name'}), 400
    
    if not email:
        return jsonify({'error': 'Missing Email'}), 400
    
    existing_user = Users.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 409

    new_user = Users.create_user(username, email)
    if new_user is None:
        return jsonify({'User not created'}), 
    else:
        return jsonify(new_user.serialize()), 200

@app.route('/user/<int:user_id>', methods=['PUT'])
def user_update(user_id):
    data = request.json
    new_username = data.get('username')
    new_email = data.get('email')

    updated_user = Users.update_user(user_id, new_username, new_email)
    if updated_user:
        return jsonify(updated_user.serialize()), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def user_delete(user_id):
    data = request.json
    user_id = data.get('id_user')

    existing_user = Users.get_user_by_id(user_id)
    if not existing_user:
        return jsonify({'error': 'Username does not exist'}), 409
    if Users.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404
    