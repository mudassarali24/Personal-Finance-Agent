from langchain.tools import tool
import json
import os
from datetime import datetime
from src.config import EXPENSES_FILE, DATA_DIR, BUDGETS_FILE, DEFAULT_CATEGORIES
import uuid

def ensure_data_directory():
    """Ensures data dir exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_expenses():
    """Loads expenses from JSON file."""
    ensure_data_directory()
    if not os.path.exists(EXPENSES_FILE):
        return {"expenses": []}

    with open(EXPENSES_FILE, 'r') as f:
        return json.load(f)

def save_expenses(data):
    """Saves expenses to JSON file."""
    ensure_data_directory()
    with open(EXPENSES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@tool
def add_expense(category: str, amount: float, description: str) -> dict:
    """Add a new expense to track spending.
    
    Use this when users wants to log, add, record, or track and expense.
    
    Parameters:
    - category (str): The category of the expense (e.g., 'food', 'transport', 'entertainment', 'utilities', 'shopping', 'health', 'education', 'other')
    - amount (float): The amount of the expense to add (must be a positive number)
    - description (str): A brief description of what the expense was for
    
    Returns:
    - dict: A dictionary containing a confirmation message with the expense details
    
    Examples:
    - User: "I spent $45.50 on groceries"
        -> add_expense(category="food", amount=45.50, description="groceries")
    
    - User: "Log $20 for uber ride"
        -> add_expense(category="transport", amount=20, description="uber ride")
    """
    if amount <= 0:
        return {"result": "Error: Amount must be greater than zero."}
    
    category = category.lower()

    if category not in DEFAULT_CATEGORIES:
        category_warning = f"(Note: '{category}' is not a standard category. Standard categories are: {', '.join(DEFAULT_CATEGORIES)})"
    else:
        category_warning = ""

    data = load_expenses()
    new_expense= {
        "id": str(uuid.uuid4()),
        "category": category,
        "amount": round(amount, 2),
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "timestamp": datetime.now().isoformat()
    }
    data["expenses"].append(new_expense)
    save_expenses(data)

    return {"result": f"Expense added successfully: ${amount:.2f} for {description} in category '{category}'{category_warning}. Total expenses: {len(data['expenses'])}"}



@tool
def get_expenses_count() -> dict:
    """Get the total numnber of expenses recorded.
    
    Returns:
    - dict: A dictionary with the total count of expenses."""
    data = load_expenses()
    count = len(data.get("expenses", []))
    if count == 0:
        return {"result": "No expenses yet!"}
    else:
        return {"result": count}
    

@tool
def get_all_expenses() -> dict:
    """Get a list of all expenses with their details.
    
    Use this when users ask to see all their expenses, view their expenses history, or list all transactions
    
    Returns:
    - dict: A formatted list of all expenses with dates, categories, amounts, and descriptions

    Examples:

    - User: 
    """

    data = load_expenses()
    expenses = data.get("expenses", [])

    if not expenses:
        return {"result": "No expenses recorded."}

    expenses_sorted = sorted(expenses, key=lambda x: x["timestamp"], reverse=True)

    result = f"Total expenses recorded: {len(expenses)}\n\n"

    for i, expense in enumerate(expenses_sorted, 1):
        result += f"{i}. [{expense['date']}] {expense['category'].upper()}: ${expense['amount']:.2f}"
        result += f"   Description: {expense['description']}\n\n"


    total = sum(exp["amount"] for exp in expenses)
    result += f"Total amount spent: ${total:.2f}"

    return {"result": result}