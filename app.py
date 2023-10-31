from flask import Flask, request, jsonify , render_template
import mysql.connector 
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': ' ',
    'database': 'expenseTracker'
}

@app.route('/add_salary', methods=['GET','POST'])
def add_salary():
    if request.method == 'POST':
        try:
            data = request.form
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
    return render_template ('addSalary.html')

@app.route('/add_expense', methods=['GET','POST'])
def add_expense():
    if request.method == 'POST':
        try:
            data = request.form
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
    return render_template ('addExpense.html')

@app.route('/calculate_balance', methods=['GET', 'POST'])
def calculate_balance():
    if request.method == "GET":
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
    return render_template ('balanceAmount.html', balance_amount = balance)
        

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='192.168.0.135', port=5000)
