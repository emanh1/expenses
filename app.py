from flask import Flask, render_template, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

CSV_FILE = 'expenses.csv'

def read_expenses():
    with open(CSV_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        expenses = list(reader)
    return expenses

def write_expenses(expenses):
    fieldnames = ['description', 'payment_type', 'amount', 'date']
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(expenses)

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
            total_expense+=float(expense['amount'])

    return render_template('index.html', total_expense=total_expense, current_date=current_date, expenses_by_month=expenses_by_month)

@app.route('/add', methods=['POST'])
def add_expense():
    description = request.form.get('description')
    payment_type = request.form.get('payment_type')
    amount = float(request.form.get('amount'))
    date_str = request.form.get('date')

    date = datetime.strptime(date_str, '%Y-%m-%d').date()

    expenses = read_expenses()

    new_expense = {
        'description': description,
        'payment_type': payment_type,
        'amount': amount,
        'date': date.strftime('%Y-%m-%d')
    }
    expenses.append(new_expense)

    write_expenses(expenses)

    return redirect('/')

@app.route('/delete/<int:index>', methods=['POST'])
def delete_expense(index):
    expenses = read_expenses()

    if 0 <= index < len(expenses):
        del expenses[index]

        write_expenses(expenses)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
