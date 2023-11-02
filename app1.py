from flask import Flask, request, jsonify , render_template
import bcrypt
import jwt
import mysql.connector 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'    

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'PASSWORD',
    'database': 'expenseTracker'
}

@app.route('/register', methods =['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username,email, password) VALUES  (%s,%s,%s)", (username,email,hash_password))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Registered successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)

