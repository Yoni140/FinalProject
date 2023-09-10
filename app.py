from flask import Flask, request

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    print(f"Registering user {username} with password {password}")
    return {'message': 'User registered'}, 201

if __name__ == '__main__':
    app.run(debug=True)
