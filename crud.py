from model import db, User, Budget, Account_History, connect_to_db
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

def create_account_history(name, account_number, phone_number, address, notes):
    
    history = Account_History(
        name=name,
        account_number=account_number,
        phone_number=phone_number,
        address=address,
        notes=notes
    )
    return history    

def get_account_history_by_id(history_id):
    return Account_History.query.get(history_id)
    
def get_account_history():
    return Account_History.query.all()

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