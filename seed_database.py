from datetime import datetime

import json
import os
import crud
import model
import server

print("Dropping Database")
os.system('dropdb budget')
print("Creating Database")
os.system('createdb budget')

model.connect_to_db(server.app)
with server.app.app_context():
    model.db.create_all()
    print("Creating account history")
    with open('data/account_history.json') as f:
        account_history_data = json.loads(f.read())

    account_history_in_db = []

    for history in account_history_data:
        name, account_number, phone_number, address, notes = (
            history["name"],
            history["account_number"],
            history["phone_number"],
            history["address"],
            history["notes"]
        )  
        last_updated = datetime.strftime(history["account_updated"], "%Y-%m-%d")
        
        db_account_history = crud.create_account_history(name, account_number, phone_number, address, notes)
        account_history_in_db.append(db_account_history)
        
    print("Adding changes to account history")    
    model.db.session.add_all(account_history_in_db)
    print("commiting changes account history")
    model.db.session.commit()

    print("Creating budget")
    with open('data/budget.json') as f:
        budget_data = json.loads(f.read())

    budget_in_db = []

    for budget in budget_data:
        income, bills, other, account_history, total = (
            budget["income"],
            budget["bills"],
            budget["other"],
            budget["account_history"],
            budget["total"]
        )
        last_updated = datetime.strptime(budget["account_changed"], "%Y-%m-%d")
        
        db_budget = crud.create_budget(income, bills, other, account_history, last_updated)
        budget_in_db.append(db_budget)

    print("Adding changes budget")     
    model.db.session.add_all(budget_in_db)
    print("commiting changes budget")
    model.db.session.commit()    