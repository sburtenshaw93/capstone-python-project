from flask import Flask, request, jsonify, render_template, flash, session, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from forms import RegistrationForm, LoginForm
from flask_cors import CORS
from datetime import timedelta
import crud
from jinja2 import StrictUndefined
from model import connect_to_db, db, User
import os


app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
app.jinja_env.undefined = StrictUndefined
login_manager = LoginManager()
login_manager.init_app(app)

# This is for the starting point for budget to have the income be zero
income = []
expense = []
remaining_balance = []


@app.route("/")
def homepage():
    login_form = LoginForm()
    registration_form = RegistrationForm()
    
    return render_template('homepage.html', login_form=login_form, registration_form=registration_form)

@app.route("/homepage")
@login_required
def homepage2():
    return render_template("homepage.html")

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
def login():
    form = LoginForm()
    user = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
    
        user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
            login_user(user, remember=remember_me, duration=timedelta(days=30))
            flash("You logged in successfully.", "success")
            return redirect("/budget")
    else:
        flash("Invaild username or password", "error")
    
    return redirect("/")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect("/")   

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

# Budget -------------------------------------------

@app.route("/budget", methods=["GET", "DELETE"])
def budget():
    
    user_input = []
    user_expense_input = []
    income = 0
    expense = 0
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
                           expense=expense, 
                           user_input=user_input,
                           remaining_balance=remaining_balance,
                           user_expense_input=user_expense_input
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
