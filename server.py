from flask import Flask, request, jsonify, render_template, flash, session, redirect
from flask_cors import CORS
import crud
from jinja2 import StrictUndefined
from model import connect_to_db, db
import os

app = Flask(__name__)
cors = CORS(app)
app.jinja_env.undefined = StrictUndefined

# This is for the starting point for budget to have the income be zero
income = []
expenses_total = []
remaining_balance = []

@app.route("/")
def homepage():
    return render_template('homepage.html')

#create account/ users / Login ------------------------

@app.route("/create-account")
def create_account():
       
    return render_template("create-page.html")

@app.route("/users", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Can't make an account with this email. Please try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account has been sucessfully created")
    return redirect("/")

@app.route("/login", methods=["POST"])
def process_login():
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect")
    else:
        session["user_email"] = user.email
        flash(f"Successfully Logged in")
    return redirect("/")    

# Budget -------------------------------------------

@app.route("/budget")
def budget():
    
    user_input = []
    expense_user_input = []
    incomes = []
    income = 0
    expenses_total = 0
    remaining_balance = 0
    budget_list = crud.get_budget()
    
    return render_template("/budget-page.html", 
                           budget_list=budget_list, 
                           income=income, 
                           expenses_total=expenses_total, 
                           user_input=user_input,
                           remaining_balance=remaining_balance,
                           incomes=incomes,
                           expense_user_input=expense_user_input
                           )

@app.route('/calculate_total', methods=['GET', 'POST'])
def calculate_total():
    expense_user_input = request.form.get('expense_user_input')
    user_input = request.form.get('user_input')
    incomes = []
    income = request.form.get('income')
    expenses_total = request.form.get('expenses')
    remaining_balance = request.form.get('remaining_balance')
    if income and expenses_total:
        try:
                income = float(income)
                expenses_total = float(expenses_total)
                remaining_balance = income - expenses_total
        except ValueError:
                error_message = "Invalid input. Please enter numeric values."
                return render_template('budget-page.html', error_message=error_message)        
    else:
        error_message = "Please enter both income and expenses."
        return render_template('budget-page.html', 
                                error_message=error_message, 
                                income=income,
                                incomes=incomes,
                                expenses_total=expenses_total,
                                remaining_balance=remaining_balance, 
                                user_input=user_input,
                                expense_user_input=expense_user_input)
    if request.method == 'POST':
            
                return render_template('budget-page.html', 
                                       remaining_balance=remaining_balance, 
                                       income=income, 
                                       expenses_total=expenses_total,
                                       user_input=user_input,
                                       expense_user_input=expense_user_input,
                                       incomes=incomes)
    return render_template('budget-page.html', 
                                       remaining_balance=remaining_balance, 
                                       income=income, 
                                       expenses_total=expenses_total,
                                       user_input=user_input,
                                       expense_user_input=expense_user_input,
                                       incomes=incomes)    


@app.route("/budget", methods=["POST"])
def get_budget():
    
    income = request.json["income_id"]
    bills = request.json["bills_id"]
    other = request.json["other_id"]
    account_history = request.json["account-history"]
    total = request.json["total"]
    crud.budget_update(income, bills, other, account_history, total)
    db.session.commit()        

# account history-------------------------------

@app.route("/account_history")
def account_history():
    
    history_list = crud.get_account_history()
    
    return render_template("/account_history.html", history_list=history_list)

@app.route("/account_history", methods=["POST"])
def get_account_history():
    
    name = request.json["name_id"]
    account_number = request.json["account_number_id"]
    phone_number = request.json["phone_number"]
    address = request.json["address"]
    notes = request.json["notes_id"]
    crud.account_history_update(name, account_number, phone_number, address, notes)
    db.session.commit()
    


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True, port = 6287, host = "localhost")
