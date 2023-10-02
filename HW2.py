from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configure Database
db_config = {
    'user': 'marroquincis3368db.ctgtbyie81ca.us - east - 1.rds.amazonaws.com',
    'password': 'MarroquinDB',
    'host': 'Adml1168',
    'database': 'MarroquinCIS3368DB',
    'raise_on_warnings': True
}

# Establish connection as a context manager
def create_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(e)
        return None

# API to fetch all animals
@app.route('/api/zoo', methods=['GET'])
def get_all_animals():
    conn = create_connection()
    if conn:
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM zoo_residents")
                rows = cursor.fetchall()
                return jsonify(rows), 200
        except Error as e:
            print(e)
        finally:
            conn.close()
    return jsonify({"error": "Database connection error"}), 500

# API to add a new animal
@app.route('/api/zoo', methods=['POST'])
def add_animal():
    try:
        new_animal = request.json
        conn = create_connection()
        if conn:
            with conn.cursor() as cursor:
                insert_query = "INSERT INTO zoo_residents (domain, kingdom, class, species, age_years, nickname, type, habitat_description, native_region, caretaker_email) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (
                    new_animal['domain'], new_animal['kingdom'], new_animal['class'], new_animal['species'],
                    new_animal['age_years'], new_animal['nickname'], new_animal['type'],
                    new_animal['habitat_description'], new_animal['native_region'], new_animal['caretaker_email']
                ))
                conn.commit()
                return "Animal added successfully!", 201
    except KeyError:
        return jsonify({"error": "Invalid JSON input"}), 400
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return jsonify({"error": "Database connection error"}), 500

# API to update an animal's active status
@app.route('/api/zoo', methods=['PUT'])
def update_animal_active_status():
    try:
        data = request.json
        animal_id = data.get('animal_id')
        active_status = data.get('active_status')
        if animal_id is None or active_status is None:
            return jsonify({"error": "Missing animal_id or active_status in JSON"}), 400
        conn = create_connection()
        if conn:
            with conn.cursor() as cursor:
                update_query = "UPDATE zoo_residents SET active_status = %s WHERE animal_id = %s"
                cursor.execute(update_query, (active_status, animal_id))
                conn.commit()
                return "Animal updated successfully!", 200
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return jsonify({"error": "Database connection error"}), 500

# API to delete an animal
@app.route('/api/zoo', methods=['DELETE'])
def delete_animal():
    try:
        data = request.json
        animal_id = data.get('animal_id')
        if animal_id is None:
            return jsonify({"error": "Missing animal_id in JSON"}), 400
        conn = create_connection()
        if conn:
            with conn.cursor() as cursor:
                delete_query = "DELETE FROM zoo_residents WHERE animal_id = %s"
                cursor.execute(delete_query, (animal_id,))
                conn.commit()
                return "Animal deleted successfully!", 200
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return jsonify({"error": "Database connection error"}), 500

if __name__ == '__main__':
    app.run(debug=True)
