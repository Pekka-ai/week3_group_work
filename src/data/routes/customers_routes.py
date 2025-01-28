from flask import Blueprint, request
from services.customer_service import db_create_customer, db_get_customers

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