from model import db, User, Budget, Account_History, connect_to_db
import os 

def create_user(username, password, email, phone_number):
    
    user = User(username=username, password=password, email=email, phone_number=phone_number)
    
    return user

def create_budget(income, user_income_input, expense, user_expense_input, other, account_history, total, type):
    budget = Budget(
        income=income,
        user_income_input=user_income_input,
        expense=expense,
        user_expense_input=user_expense_input, 
        other=other,
        account_history=account_history,
        total=total,
        type=type
    )
    db.session.add(budget)
    db.session.commit()
    return budget

def delete_budget(budget_id):
    budget = Budget.query.get(budget_id)
    db.session.delete(budget)
    db.session.commit()


def create_account_history(name, account_number, phone_number, address, notes, budget_id):
    history = Account_History(
        name=name,
        account_number=account_number,
        phone_number=phone_number if phone_number else 0,
        address=address,
        notes=notes
    )
    db.session.add(history)
    budget = Budget.query.get(budget_id)
    budget.account_history = history.history_id
    db.session.commit()
    return history    

def account_history_update(account_history, name, account_number, phone_number, address, notes):
    history = Account_History.query.get(account_history)
    history.name = name
    history.account_number = account_number
    history.phone_number = phone_number if phone_number else 0
    history.address = address
    history.notes = notes
    db.session.commit()
    return history

def get_account_history_by_id(history_id):
    return Account_History.query.get(history_id)
    
def get_account_history():
    return Account_History.query.all()

def budget_update(income, bills, other, account_history, total):
    return Budget.query.get(income, bills, other, account_history, total)

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