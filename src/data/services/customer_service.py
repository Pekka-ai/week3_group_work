import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_storage_credentials
import json
from flask import jsonify

def db_get_customers():
    command=(
        """
        SELECT * FROM customers;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(command)
                customers = cur.fetchall()
                return json.dumps({"customers_list": customers})
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 


def db_get_customer_by_id(id):
    command=(
        """
        SELECT * FROM customers WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (id,))
                row = cur.fetchone()
                if row is None:
                    return jsonify({"error": "Customer not found"}), 404
                return jsonify(row)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 

def db_create_customer(name:str):
    command=(
        """
        INSERT INTO customers (name) VALUES (%s);
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (name,))
                conn.commit()
                result = {"success": "created customer name: %s " % name}
                return json.dumps(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)


def db_update_customer(id: int, name:str):
    command=(
        """
        UPDATE customers SET name = %s WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (name, id))
                conn.commit()
                if cur.rowcount == 0:
                        return jsonify({"error": "Customer not found"}), 404
                result = {"success": "updated customer id: %s " % id}
                return jsonify(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 


def db_delete_customer(id:int):
    command=(
        """
        DELETE FROM customers WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (int(id),)) 
                conn.commit()
                if cur.rowcount == 0:
                   return jsonify({"error": "Customer not found"}), 404
                result = {"success": "deleted customer id: %s" % id}
                return jsonify(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)


if __name__ == "__main__":
    print(db_get_customers())
    #print(db_create_customer("Microsoft"))
