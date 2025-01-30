from flask import Blueprint, request
from services.consultant_service import db_create_consultant, db_get_consultants

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
    