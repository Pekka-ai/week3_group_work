from flask import Blueprint, request
from services.consultant_sessions_service import db_delete_consultant_session, db_get_consultant_sessions, db_create_consultant_session, db_update_consultant_session
from flask import jsonify

consultant_sessions_bp = Blueprint('consultant_sessions', __name__)

@consultant_sessions_bp.route('/consultant_sessions', methods=['GET'])
def get_consultant_sessions():
    try:  
        return db_get_consultant_sessions()
    except:
        return {"error": "no data"}
    
@consultant_sessions_bp.route("/consultant_sessions", methods=['POST'])
def create_consultant_session():
    try: 
        data = request.get_json()
        start = data['start']
        end = data['end']
        lunch_break = data['lunch_break']
        consultant_id = data['consultant_id']
        customer_id = data['customer_id']
        result = db_create_consultant_session(start, end, lunch_break, consultant_id, customer_id)

        if isinstance(result, tuple):
            return result

        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error creating consultant_session"}), 500
    
@consultant_sessions_bp.route("/consultant_sessions/<int:id>", methods=['PUT'])
def update_consultant_session(id):
    try:
        data = request.get_json()
        start = data['start']
        end = data['end']
        lunch_break = data['lunch_break']
        consultant_id = data['consultant_id']
        customer_id = data['customer_id']
        
        result = db_update_consultant_session(id, start, end, lunch_break, consultant_id, customer_id)

        if isinstance(result, tuple):
            return result

        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error updating consultant session"}), 500
    

@consultant_sessions_bp.route("/consultant_sessions/<int:id>", methods=['DELETE'])
def delete_consultant_session(id):
    try:
        result = db_delete_consultant_session(id)
        if isinstance(result, tuple):
            return result
        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error deleting consultant session"}), 500