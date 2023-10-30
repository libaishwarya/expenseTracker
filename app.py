from flask import Flask, request, jsonify 
import mysql.connector 
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'PASSWORD',
    'database': 'expenseTracker'
}

@app.route('/add_salary', methods=['POST'])
def add_salary():
    try:
        data = request.json
        description = data['description']
        amount = float(data['amount'])
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO salary (description, amount) VALUES (%s,%s)', (description, amount))
        conn.commit()
        conn.close()
        return jsonify(message='Salary added successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        data = request.json
        description = data['description']
        amount = float(data['amount'])
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (description, amount) VALUES (%s, %s)', (description, amount))
        conn.commit()
        conn.close()
        return jsonify(message='Expense added successfully'), 201
    except Exception as e:
        return jsonify(error=str(e)), 400

@app.route('/calculate_balance', methods=['GET'])
# def calculate_balance():
#     try:
#         conn = mysql.connector.connect(**db_config)
#         cursor = conn.cursor()
#         cursor.execute('SELECT SUM(amount) FROM salary')
#         # salary_total = cursor.fetchone()[0] or 0
#         result_1 = cursor.fetchone()
#         if result_1 is not None:
#             salary_total = result_1[0]
#         else:
#             salary_total = 0

#         cursor.execute('SELECT SUM(amount) FROM expenses')
#         # expenses_total = cursor.fetchone()[0] or 0
#         result_2 = cursor.fetchone()
#         if result_2 is not None:
#             expenses_total = result_2[0]
#         else:
#             expenses_total = 0

#         balance = salary_total - expenses_total

#         conn.close()
#         return jsonify(salary_total=salary_total, expenses_total=expenses_total, balance=balance)
#     except Exception as e:
#         return jsonify(error=str(e)), 500

def calculate_balance():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute('SELECT IFNULL(SUM(amount), 0) FROM salary')
        salary_total = cursor.fetchone()[0]

        cursor.execute('SELECT IFNULL(SUM(amount), 0) FROM expenses')
        expenses_total = cursor.fetchone()[0]

        balance = salary_total - expenses_total

        conn.close()
        return jsonify(salary_total=salary_total, expenses_total=expenses_total, balance=balance)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
