from flask import Blueprint, request, jsonify, render_template
from marshmallow import ValidationError
from api.models import Plant
from api.schemas import plant_schema, plants_schema
from api import db

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/plants', methods=['GET'])
def get_plants():
    plants = Plant.query.order_by(Plant.id.desc()).all()
    return jsonify(plants_schema.dump(plants))

@bp.route('/api/plants', methods=['POST'])
def create_plant():
    json_data = request.get_json()
    if not json_data:
        return jsonify({'error': 'No input data provided'}), 400

    try:
        # Validate and deserialize input
        new_plant = plant_schema.load(json_data)
    except ValidationError as err:
        return jsonify({'error': 'Validation Error', 'messages': err.messages}), 422

    db.session.add(new_plant)
    db.session.commit()
    
    return jsonify(plant_schema.dump(new_plant)), 201

@bp.route('/api/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    plant = Plant.query.get_or_404(plant_id)
    db.session.delete(plant)
    db.session.commit()
    return jsonify({'message': 'Plant deleted successfully'}), 200
