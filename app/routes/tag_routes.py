from app import app
from flask import jsonify, request
from app.services.tags import Tags


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