from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    username = db.Column(db.Text, unique=True)
    phone_number = db.Column(db.Integer)
    is_active = db.Column(db.Boolean)
    
    def __init__(self, username, password, email, phone_number):
        self.username = username
        self.password = password
        self.email = email
        self.phone_number = phone_number
        self.is_active = True
    def check_password(self, password):
        return password == self.password
    def get_id(self):
        return self.user_id    
    
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Budget(db.Model):
    
    __tablename__ = "budgets"
    
    budget_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_income_input = db.Column(db.Text)
    income = db.Column(db.Integer)
    user_expense_input = db.Column(db.Text)
    expense = db.Column(db.Integer)
    other = db.Column(db.Integer) 
    account_history = db.Column(db.Text)
    total = db.Column(db.Integer)
    remaining_balance = db.Column(db.Integer)
    type = db.Column(db.Text)   
    
    def __repr__(self):
        return f"<Monthly income={self.income} left over income={self.remaining_balance}>"

class Account_History(db.Model):
    
    __tablename__ = "account_history"
    
    history_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)
    account_number = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f"<Account history_id={self.name}>"

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
