function deleteBudget(event) {
    event.preventDefault()
    fetch("http://localhost:6287/delete-budget/" + event.target.dataset.budgetId, {method:"DELETE", headers:{"Content-Type": "application/json"}} )
    window.location.href = 'http://localhost:6287/budget'
}
function addIncomeField() {
    const incomeFields = document.getElementById('income-fields');
    const newLabel = document.createElement('label');
    newLabel.innerHTML = 'Income:';
    incomeFields.appendChild(newLabel)
    const newTextInput = document.createElement('input');
    newTextInput.type = 'text';
    newTextInput.name = 'new_user_input';
    newTextInput.className = 'user_input';
    incomeFields.appendChild(newTextInput)
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.name = 'new-income';
    newInput.className = 'income-input';
    incomeFields.appendChild(newInput);
    const incomeDeleteButton = document.createElement('button');
    incomeDeleteButton.name = 'income-delete-button';
    incomeDeleteButton.className = 'delete-button';
    incomeDeleteButton.innerHTML = "Delete"
    incomeDeleteButton.onclick=deleteIncome
    incomeFields.appendChild(incomeDeleteButton);
}

function addExpenseField(event) {
    const expenseFields = document.getElementById('expense-fields');
    const newLabel = document.createElement('label');
    newLabel.innerHTML = 'Expense:';
    expenseFields.appendChild(newLabel)
    const newExpenseTextInput = document.createElement('input');
    newExpenseTextInput.type = 'text';
    newExpenseTextInput.name = 'new_expense_user_input';
    newExpenseTextInput.className = 'expense_user_input';
    expenseFields.appendChild(newExpenseTextInput)
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.name = 'new-expense';
    newInput.className = 'expense-input';
    expenseFields.appendChild(newInput);
    const expenseDeleteButton = document.createElement('button');
    expenseDeleteButton.name = 'expense-delete-button';
    expenseDeleteButton.className = 'delete-button';
    expenseDeleteButton.innerHTML = "Delete"
    expenseDeleteButton.onclick=deleteExpense
    expenseFields.appendChild(expenseDeleteButton);
}