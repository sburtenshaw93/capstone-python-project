from flask import Flask, request, jsonify, render_template, flash, session, redirect
from flask_cors import CORS
import crud
from model import connect_to_db, db
import os

app = Flask(__name__)
cors = CORS(app)

@app.route("/")
def homepage():
    return render_template('homepage.html')

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

@app.route("/budget")
def budget():
    
    budget_list = crud.get_budget()
    
    return render_template("/budget-page.html", budget_list=budget_list)

@app.route("/budget", methods=["POST"])
def get_budget():
    
    income = request.json["income_id"]
    bills = request.json["bills_id"]
    other = request.json["other_id"]
    account_history = request.json["account-history"]
    left_over = request.json["left-over"]
    crud.budget_update(income, bills, other, account_history, left_over)
    db.session.commit()  
    
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
