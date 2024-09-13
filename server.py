from flask import Flask, request, jsonify 

app = Flask(__name__)

users = {"Admin":"a234"}

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if users.get(username) == password: 
        return jsonify({"message":"Login successful"}), 200
    else:
        return jsonify({"mesage":"login failed"}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout successful"}), 200 

@app.route('/users', methods=['GET'])
def get_user():
    return jsonify(list(users.keys())), 200

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    users[username] = password
    return jsonify({"message": "User added successfully"}), 201


@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        del users[username]
        return jsonify({"message": "User deleted successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


if __name__ == '__main__':
    #app.run(host='127.0.0.xxxx', port=5000)
     app.run(debug=True)