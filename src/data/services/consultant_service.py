import psycopg2
from psycopg2.extras import RealDictCursor
from config import get_storage_credentials
import json
from flask import jsonify

def db_get_consultants():
    command=(
        """
        SELECT * FROM consultants;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(command)
                consultants = cur.fetchall()
                return json.dumps({"consultants_list": consultants})
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 

def db_create_consultant(name:str):
    command=(
        """
        INSERT INTO consultants (name) VALUES (%s);
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (name,))
                conn.commit()
                result = {"success": "created consultant name: %s " % name}
                return json.dumps(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)


def db_get_consultant_by_id(id):
    command=(
        """
        SELECT * FROM consultants WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (id,))
                row = cur.fetchone()
                if row is None:
                    return jsonify({"error": "Consultant not found"}), 404
                return jsonify(row)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 


def db_update_consultant(id:int, name:str):
    command=(
        """
        UPDATE consultants SET name = %s WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (name, id))
                conn.commit()
                if cur.rowcount == 0:
                        return jsonify({"error": "Consultant not found"}), 404
                result = {"success": "updated consultant id: %s " % id}
                return jsonify(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 


def db_delete_consultant(id:int):
    command=(
        """
        DELETE FROM consultants WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**get_storage_credentials()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (int(id),)) 
                conn.commit()
                if cur.rowcount == 0:
                   return jsonify({"error": "Consultant not found"}), 404
                result = {"success": "deleted consultant id: %s" % id}
                return jsonify(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)



if __name__ == "__main__":
    print(db_get_consultants())
    #print(db_create_consultant("Katy Tao"))
    #print(db_update_consultant("Jane Doe", 1))
    