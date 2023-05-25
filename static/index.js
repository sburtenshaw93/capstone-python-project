function deleteIncome(event) {
    event.preventDefault()
}
function addIncomeField() {
    const incomeFields = document.getElementById('income-fields');
    const newTextInput = document.createElement('input');
    newTextInput.type = 'text';
    newTextInput.name = 'user_input';
    newTextInput.className = 'user_input';
    incomeFields.appendChild(newTextInput)
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.name = 'income';
    newInput.className = 'income-input';
    incomeFields.appendChild(newInput);
    const incomeDeleteButton = document.createElement('button');
    incomeDeleteButton.name = 'income-delete-button';
    incomeDeleteButton.className = 'delete-button';
    incomeDeleteButton.innerHTML = "Delete"
    incomeDeleteButton.onclick=deleteIncome
    incomeFields.appendChild(incomeDeleteButton);
}
function deleteExpense(event) {
    event.preventDefault()
}
function addExpenseField(event) {
    const expenseFields = document.getElementById('expense-fields');
    const newExpenseTextInput = document.createElement('input');
    newExpenseTextInput.type = 'text';
    newExpenseTextInput.name = 'expense_user_input';
    newExpenseTextInput.className = 'expense_user_input';
    expenseFields.appendChild(newExpenseTextInput)
    const newInput = document.createElement('input');
    newInput.type = 'number';
    newInput.name = 'expense';
    newInput.className = 'expense-input';
    expenseFields.appendChild(newInput);
    const expenseDeleteButton = document.createElement('button');
    expenseDeleteButton.name = 'expense-delete-button';
    expenseDeleteButton.className = 'delete-button';
    expenseDeleteButton.innerHTML = "Delete"
    expenseDeleteButton.onclick=deleteExpense
    expenseFields.appendChild(expenseDeleteButton);
}