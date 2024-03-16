from app import app
from flask import jsonify, request
from app.services.locations import Locations

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
