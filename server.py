from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
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

@app.route("/budget", methods=["GET", "DELETE"])
def budget():
    
    user_input = []
    expense_user_input = []
    income = 0
    expenses_total = 0
    remaining_balance = 0
    budget_list = crud.get_budget()
    
    for budget in budget_list:
        if budget.type == "income":
            remaining_balance = remaining_balance + budget.income
        else:
            remaining_balance = remaining_balance - budget.expense      
    return render_template("/budget-page.html", 
                           budget_list=budget_list, 
                           income=income, 
                           expenses_total=expenses_total, 
                           user_input=user_input,
                           remaining_balance=remaining_balance,
                           expense_user_input=expense_user_input
                           )

@app.route('/calculate_total', methods=['POST'])
def calculate_total():
    new_incomes = request.form.getlist('new-income')
    new_user_income_inputs = request.form.getlist('new_user_input')
    for i in range(len(new_incomes)):
        new_income = new_incomes[i]
        new_user_income_input = new_user_income_inputs[i]
        crud.create_budget(new_income, new_user_income_input, None, None, None, "", 0, "income")
    new_expenses = request.form.getlist('new-expense')
    new_user_expense_inputs = request.form.getlist('new_expense_user_input')
    for i in range(len(new_expenses)):
        new_expense = new_expenses[i]
        new_user_expense_input = new_user_expense_inputs[i]
        crud.create_budget(None, None, new_expense, new_user_expense_input, None, "", 0, "expense")     
    return redirect(url_for("budget"))
     
@app.route('/delete-budget/<budget_id>', methods=["GET", "DELETE"])
def delete_budget(budget_id):
    crud.delete_budget(budget_id) 

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
