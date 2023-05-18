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

with open('data/budget.json') as f:
    budget_data = json.loads(f.read())

budget_in_db = []

for budget in budget_data:
    income, bills, other, account_history = (
        budget["income"],
        budget["bills"],
        budget["other"],
        budget["account_history"]
    )
    last_updated = datetime.strptime(budget["account_changed"], "%Y-%m-%d")
    
    db_budget = crud.create_budget(income, bills, other, account_history, last_updated)
    budget_in_db.append(db_budget)
model.db.session.add_all(budget_in_db)
model.db.session.commit()    