from datetime import datetime

import json
import os
import crud
import model
import server

os.system('dropdb budget')
os.system('createdb budget')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/account_history,json') as f:
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
model.db.session.add_all(account_history_in_db)
model.db.session.commit()      

with open('data/budget.json') as f:
    budget_data = json.loads(f.read())

budget_in_db = []

for budget in budget_data:
    income, bills, other, account_history, left_over = (
        budget["income"],
        budget["bills"],
        budget["other"],
        budget["account_history"],
        budget["left_over"]
    )
    last_updated = datetime.strptime(budget["account_changed"], "%Y-%m-%d")
    
    db_budget = crud.create_budget(income, bills, other, account_history, last_updated)
    budget_in_db.append(db_budget)
model.db.session.add_all(budget_in_db)
model.db.session.commit()    