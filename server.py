from flask import Flask, request, jsonify 
import sqlite3 


app = Flask(__name__)

# crear la base de datos y la tabla de usuarios si no existen 
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS  users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nombre TEXT NOT NULL, 
            edad INTEGER NOT NULL, 
            telefono TEXT NOT NULL, 
            email TEXT NOT NULL, 
            username TEXT UNIQUE NOT NULL, 
            password TEXT NOT NULL
        )
    ''')
    # Agregar el ususario admin si no existe 
    cursor.execute('''
        INSERT OR IGNORE INTO users (nombre, edad, telefono, email, username, password)
        VALUES ('Admin', 30, '123456789', 'admin@example.com', 'Admin', 'a2345')
    ''')
    conn.commit()
    conn.close() 

init_db()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Login failed"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"}), 200 

@app.route('/users', methods=['GET'])
def get_user():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, edad, telefono, email, username FROM users")
    users = cursor.fetchall() 
    conn.close() 

    return jsonify(users), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    nombre = data.get('nombre')
    edad = data.get('edad')
    telefono = data.get('telefono')
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute(''' 
            INSERT INTO users (nombre, edad, telefono, email, username, password)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (nombre, edad, telefono, email, username, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"message": "User already exists"}), 400


@app.route('/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "User deleted successfully"}), 200



if __name__ == '__main__':
    #app.run(host='127.0.0.xxxx', port=5000)
     app.run(debug=True)