from app import app
from flask import jsonify, request
from app.services.history import History

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

