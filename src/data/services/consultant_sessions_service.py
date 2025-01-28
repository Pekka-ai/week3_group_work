from datetime import datetime
from flask import jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
from config import config
from services.customer_service import db_get_customer_by_id
from services.consultant_service import db_get_consultant_by_id


def db_get_consultant_sessions():
    command=(
        """
        SELECT * FROM consultant_sessions;
        """)
    try:
        with psycopg2.connect(**config()) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(command)
                consultant_sessions = cur.fetchall()
                conn.commit()
                return jsonify({"consultant_sessions_list": consultant_sessions})
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 


def db_create_consultant_session(start:datetime, end:datetime, lunch_break:int, consultant_id:int, customer_id:int):
    check_consultant=db_get_consultant_by_id(consultant_id)
    check_customer=db_get_customer_by_id(customer_id)
    
    if isinstance(check_consultant, tuple) and check_consultant[1] == 404:
        return check_consultant

    elif isinstance(check_customer, tuple) and check_customer[1] == 404:
        return check_customer

    else: 
        command=(
            """
            INSERT INTO consultant_sessions 
            (start_time, end_time, lunch_break, consultant_id, customer_id) 
            VALUES (%s,%s,%s,%s,%s);
            """)
        try:
            with psycopg2.connect(**config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(command, (start,end,lunch_break,consultant_id,customer_id))
                    conn.commit()
                    result = {"success": "created consultant session with consultant_id: %s " % consultant_id}
                    return jsonify(result)
        except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return jsonify({"error": str(error)}), 500


def db_get_consultant_session_by_id(id):
    command=(
        """
        SELECT * FROM consultant_sessions WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**config()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (id,))
                conn.commit()
                row = cur.fetchone()
                if row is None:
                    return jsonify({"error": "Consultant session not found"}), 404
                return jsonify(row)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error) 
            return jsonify({"error": "Database error"}), 500


def db_update_consultant_session(id: int, start:datetime, end:datetime, lunch_break:int, consultant_id:int, customer_id:int):
    check_consultant=db_get_consultant_by_id(consultant_id)
    check_customer=db_get_customer_by_id(customer_id)

    if isinstance(check_consultant, tuple) and check_consultant[1] == 404:
        return check_consultant

    elif isinstance(check_customer, tuple) and check_customer[1] == 404:
        return check_customer

    else:
        command=(
            """
            UPDATE consultant_sessions 
            SET start_time = %s, end_time =%s, lunch_break = %s, consultant_id = %s , customer_id = %s WHERE id = %s;
            """)
        try:
            with psycopg2.connect(**config()) as conn:
                with conn.cursor() as cur:
                    cur.execute(command, (start,end,lunch_break,consultant_id,customer_id, id))
                    conn.commit()
                    if cur.rowcount == 0:
                        return jsonify({"error": "Consultant session not found"}), 404
                    result = {"success": "updated consultant_session id: %s " % id}
                    return jsonify(result)
        except (psycopg2.DatabaseError, Exception) as error:
                print(error)
                return jsonify({"error": "Database error"}), 500


def db_delete_consultant_session(id:int):
    command=(
        """
        DELETE FROM consultant_sessions WHERE id = %s;
        """)
    try:
        with psycopg2.connect(**config()) as conn:
            with conn.cursor() as cur:
                cur.execute(command, (id,))
                conn.commit()
                if cur.rowcount == 0:
                   return jsonify({"error": "Consultant session not found"}), 404
                result = {"success": "deleted consultant session id: %s" % id}
                return jsonify(result)
    except (psycopg2.DatabaseError, Exception) as error:
            print(error)
            return jsonify({"error": "Database error"}), 500
    

if __name__ == "__main__":
    """
    start_time = datetime(2025, 1, 28, 10, 0, 0)
    end_time = datetime(2025, 1, 28, 12, 0, 0)
    lunch_break = 30
    consultant_id = 4
    customer_id = 2

    # Call the function
    response = db_create_consultant_session(start_time, end_time, lunch_break, consultant_id, customer_id)
    print(response)
    """


    print(db_get_consultant_session_by_id(1))
        