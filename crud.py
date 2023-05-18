from model import db, User, Budget, connect_to_db
import os 

def create_user(email, password):
    
    user = User(email=email, password=password)
    
    return user

def create_budget(income, bills, other, account_history, left_over):
    
    budget = Budget(
        income=income,
        bills=bills, 
        other=other,
        account_history=account_history,
        left_over=left_over
    )
    return budget

def get_budget():
    return Budget.query.all()

def get_users():
    return User.query.all()

def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter(User.email == email).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)