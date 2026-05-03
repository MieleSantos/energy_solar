from flask import Blueprint, request, jsonify, render_template
from api.exceptions import ApiError
from api.schemas import plant_schema, plants_schema
from api.services.plant_service import create_plant as create_plant_service
from api.services.plant_service import delete_plant as delete_plant_service
from api.services.plant_service import list_plants

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/plants', methods=['GET'])
def get_plants():
    plants = list_plants()
    return jsonify(plants_schema.dump(plants))

@bp.route('/api/plants', methods=['POST'])
def create_plant():
    json_data = request.get_json(silent=True)
    if not json_data:
        raise ApiError("No input data provided", status_code=400)

    new_plant = create_plant_service(json_data)
    return jsonify(plant_schema.dump(new_plant)), 201

@bp.route('/api/plants/<int:plant_id>', methods=['DELETE'])
def delete_plant(plant_id):
    delete_plant_service(plant_id)
    return jsonify({'message': 'Plant deleted successfully'}), 200
