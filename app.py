from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_FILE = 'expenses.db'

def read_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()

    expenses_list = []
    for expense in expenses:
        expenses_list.append({
            'id': expense[0],
            'description': expense[1],
            'payment_type': expense[2],
            'amount': expense[3],
            'date': expense[4]
        })

    return expenses_list

def add_expense_to_db(expense):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, payment_type, amount, date) VALUES (?, ?, ?, ?)",
                   (expense['description'], expense['payment_type'], expense['amount'], expense['date']))
    conn.commit()
    conn.close()

def delete_expense_from_db(expense_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    current_date = datetime.now().strftime("%m-%Y")
    expenses = read_expenses()

    expenses_by_month = {}
    total_expense = 0
    for expense in expenses:
        date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
        month_year = date_obj.strftime('%m-%Y')

        if month_year not in expenses_by_month:
            expenses_by_month[month_year] = []

        expenses_by_month[month_year].append(expense)

    for expense in expenses_by_month.get(current_date, []):
        total_expense += float(expense['amount'])

    return render_template('index.html', total_expense=total_expense, current_date=current_date, expenses_by_month=expenses_by_month)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form.get('description')
    payment_type = request.form.get('payment_type')
    amount = float(request.form.get('amount'))
    date_str = request.form.get('date')

    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    new_expense = {
        'description': description,
        'payment_type': payment_type,
        'amount': amount,
        'date': date.strftime('%Y-%m-%d')
    }

    add_expense_to_db(new_expense)

    return redirect('/')

@app.route('/delete/<int:expense_id>', methods=['POST'])
def delete_expense(expense_id):
    delete_expense_from_db(expense_id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
