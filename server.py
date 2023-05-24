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
total = []

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
    
    total = []
    budget_list = crud.get_budget()
    
    return render_template("/budget-page.html", budget_list=budget_list, total=total)

@app.route('/calculate_total', methods=['POST'])
def calculate_total():
    income_values = request.form.getlist('income')
    expense_values = request.form.getlist('expense')

    total = 0
    for income in income_values:
        try:
            total += float(income)
        except ValueError:
            pass  # Skip invalid values

    for expense in expense_values:
        try:
            total -= float(expense)
        except ValueError:
            pass # Skip invalid values

    return render_template('budget-page.html', total=total)


@app.route("/budget", methods=["POST"])
def get_budget():
    
    income = request.json["income_id"]
    bills = request.json["bills_id"]
    other = request.json["other_id"]
    account_history = request.json["account-history"]
    total = request.json["total"]
    crud.budget_update(income, bills, other, account_history, total)
    db.session.commit()  

# @app.route('/add_income', methods=["POST"])
# def add_income():
#     global total   
#     income = int(request.form['income'])
#     total += income
#     return render_template('budget-page.html', total=total)
 
# @app.route('/subtract_expense', methods=["POST"])
# def subtract_expense():
#     global total
#     expense = int(request.form['expense'])
#     total = expense
#     return render_template('budget-page.html')       

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
