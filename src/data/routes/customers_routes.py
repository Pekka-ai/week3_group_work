from flask import Blueprint, request
from services.customer_service import db_create_customer, db_delete_customer, db_get_customers, db_update_customer
from flask import jsonify

customers_bp = Blueprint('customers', __name__)

@customers_bp.route('/customers', methods=['GET'])
def get_customers():
    try:  
        return db_get_customers()
    except:
        return {"error": "no data"}
    

@customers_bp.route('/customers', methods=['POST'])
def create_customer():
    try: 
        data = request.get_json()
        name = data['name']
        db_create_customer(name)
        return {"success": "created customer: %s" % name}
    except:
        return {"error": "error creating customer"}
    

@customers_bp.route("/customers/<int:id>", methods=['PUT'])
def update_customer(id):
    try:
        data = request.get_json()
        name = data['name']
        result = db_update_customer(id, name)

        if isinstance(result, tuple):
            return result

        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error updating customer"}), 500
    

@customers_bp.route("/customers/<int:id>", methods=['DELETE'])
def delete_customer(id):
    try:
        result = db_delete_customer(id)
        if isinstance(result, tuple):
            return result
        return result, 201

    except Exception as e:
        print(e)
        return jsonify({"error": "Error deleting customer"}), 500