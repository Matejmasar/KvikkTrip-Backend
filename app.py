from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import webbrowser
import threading
from database import db
from src.locations import Locations
from src.tags import Tags
from src.users import Users
from src.history import History
from src.preferences import Preferences

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://admin:kvikktrip_password@dpg-cnevjqi1hbls738raqa0-a.frankfurt-postgres.render.com/kvikktrip'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis;'))
    db.session.commit()

with app.app_context():
    db.create_all()

''' Opens a web browser to view the backend'''
def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

''' Default route '''
@app.route('/')
def index():
    return "Kvikk Trip Backend"


''' 
CRUD API for Location table
'''
@app.route('/location', methods=['GET'])
@app.route('/locations', methods=['GET'])
def location_get_all():
    all_locations = Locations.get_all_locations()
    if all_locations is None or len(all_locations) == 0:
        return "There are no locations in the database"
    else:
        return jsonify([location.serialize() for location in all_locations])

@app.route('/location/<int:id_location>', methods=['GET'])
def location_get(id_location):
    the_location = Locations.get_location_by_id(id_location)
    if the_location is None:
        return jsonify({"message":"The location is not registered"}), 400
    else:
        return jsonify(the_location.serialize()), 200

@app.route('/location', methods=['POST'])
def location_post():
    data = request.json
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not name or not latitude or not longitude:
        return jsonify({'error': 'Missing required fields'}), 400
    
    new_location = Locations.add_location(name, latitude, longitude)
    if new_location:
        return jsonify(new_location), 201
    else:
        # Handle the case where the location could not be added
        return jsonify({'error': 'Unable to create the location'}), 500

@app.route('/location/<int:id_location>', methods=[ 'PUT'])
def location_put(id_location):
    data = request.json
    name = data.get('name')
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    updated_location = Locations.update_location(id_location, name, latitude, longitude)
    if updated_location:
        return jsonify(updated_location.serialize())
    else:
        return jsonify({'error': 'Location not found'}), 404

@app.route('/location/<int:id_location>', methods=[ 'DELETE'])
def location_delete(id_location):
    if Locations.delete_location(id_location):
        return jsonify({'message': 'Location deleted successfully'}), 200
    else:
        return jsonify({'error': 'Location not found'}), 404
    
# Relationship method: Add a tag to a location
@app.route('/locations/<int:id_location>/tags', methods=['POST'])
def add_tag_to_location(id_location):
    data = request.json
    label = data.get('label')

    location = Locations.query.get(id_location)
    if not location:
        return jsonify({'error': 'Location not found'}), 404

    new_tag = location.add_tag(label)
    return jsonify(new_tag.serialize()), 201    



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
    

'''
 CRUD API for History table
'''
@app.route('/events', methods=['GET'])
def get_all_events():
    all_events = History.get_all_events()
    if all_events is None or len(all_events) == 0:
        return jsonify({'There are no events in the database'}), 200
    else:
        return jsonify([event.serialize() for event in all_events]), 200

@app.route('/event', methods=['POST'])
@app.route('/events', methods=['POST'])
def event_post():
    data = request.json
    weight = data.get('weight')

    if not weight:
        return jsonify({'error': 'Missing weight field'}), 400

    existing_event = History.does_exists(weight) #query.filter_by(weight=weight).first()
    if existing_event:
        return jsonify({'error': 'Event already exists'}), 409
    
    new_event = History.add_event(weight)
    return jsonify(new_event.serialize()), 201

@app.route('/event/<int:id_event>', methods=['PUT'])
def event_put(id_event):
    data = request.json
    new_weight = data.get('weight')

    existing_event = History.get_event(id_event) #query.filter_by(weight=weight).first()
    if not existing_event:
        return jsonify({'error': 'Event does not exist, cannot update'}), 409
    
    updated_event = History.update_event(id_event, new_weight)
    if updated_event:
        return jsonify(updated_event.serialize())
    else:
        return jsonify({'error': 'Event not found'}), 404

@app.route('/event/<int:id_event>', methods=['DELETE'])
def event_delete(id_event):

    existing_event = History.get_event(id_event) #query.filter_by(weight=weight).first()
    if not existing_event:
        return jsonify({'error': 'Event does not exist, cannot delete'}), 409
   
    if History.delete_event(id_event):
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'error': 'Event not found'}), 404


'''
 CRUD API for Tags table
'''
@app.route('/tags', methods=['GET'])
@app.route('/tag', methods=['GET'])
def get_all_tags():
    all_tags = Tags.get_all_tags()
    if all_tags is None or len(all_tags) == 0:
        return jsonify({'There are no tags in the database'}), 200
    else:
        return jsonify([tag.serialize() for tag in all_tags]), 200

@app.route('/tag/<int:id_tag>', methods=['GET'])
def tag_get(id_tag):
    tag = Tags.get_tab_by_id(id_tag)
    return jsonify([tag.serialize()])

@app.route('/tag', methods=['POST'])
@app.route('/tags', methods=['POST'])
def tag_post():
    data = request.json
    label = data.get('label')

    if not label:
        return jsonify({'error': 'Missing label field'}), 400

    existing_tag = Tags.does_exists(label) #query.filter_by(label=label).first()
    if existing_tag:
        return jsonify({'error': 'Tag already exists'}), 409
    
    new_tag = Tags.add_tag(label)
    return jsonify(new_tag.serialize()), 201

@app.route('/tag/<int:id_tag>', methods=['PUT'])
def tag_put(id_tag):
    data = request.json
    new_label = data.get('label')

    existing_tag = Tags.get_tag(id_tag) #query.filter_by(label=label).first()
    if not existing_tag:
        return jsonify({'error': 'Tag does not exist, cannot update'}), 409
    
    updated_tag = Tags.update_tag(id_tag, new_label)
    if updated_tag:
        return jsonify(updated_tag.serialize())
    else:
        return jsonify({'error': 'Tag not found'}), 404

@app.route('/tag/<int:id_tag>', methods=['DELETE'])
def tag_delete(id_tag):

    existing_tag = Tags.get_tag(id_tag) #query.filter_by(label=label).first()
    if not existing_tag:
        return jsonify({'error': 'Tag does not exist, cannot delete'}), 409
   
    if Tags.delete_tag(id_tag):
        return jsonify({'message': 'Tag deleted successfully'})
    else:
        return jsonify({'error': 'Tag not found'}), 404

                
if __name__ == '__main__':
    #browser_thread = threading.Thread(target=open_browser)
    #browser_thread.start()
    app.run(debug=True)