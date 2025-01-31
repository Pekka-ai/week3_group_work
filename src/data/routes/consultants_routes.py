from flask import Blueprint, request
from services.consultant_service import db_create_consultant, db_delete_consultant, db_get_consultants, db_update_consultant
from flask import jsonify

consultants_bp = Blueprint('consultants', __name__)

@consultants_bp.route('/consultants', methods=['GET'])
def get_consultants():
    try:  
        return db_get_consultants()
    except:
        return {"error": "no data"}
    


@consultants_bp.route("/consultants", methods=['POST'])
def create_consultant():
    try: 
        data = request.get_json()
        name = data['name']
        db_create_consultant(name)
        return {"success": "created consultant: %s" % name}
    except:
        return {"error": "error creating consultant"}


@consultants_bp.route("/consultants/<int:id>", methods=['PUT'])
def update_consultant(id):
    try:
        data = request.get_json()
        name = data['name']
        result = db_update_consultant(id, name)

        if isinstance(result, tuple):
            return result

        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error updating consultant"}), 500
    

@consultants_bp.route("/consultants/<int:id>", methods=['DELETE'])
def delete_consultant(id):
    try:
        result = db_delete_consultant(id)
        if isinstance(result, tuple):
            return result
        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error deleting consultant"}), 500
    