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
    
    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

class Budget(db.Model):
    
    __tablename__ = "budgets"
    
    budget_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    income = db.Column(db.Integer)
    bills = db.Column(db.Integer)
    other = db.Column(db.Integer) 
    account_history = db.Column(db.Text)
    left_over = db.Column(db.Integer)   
    
    def __repr__(self):
        return f"Monthly income={self.income} left over income={self.left_over}"

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app)
