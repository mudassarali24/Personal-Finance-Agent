from langchain.tools import tool
import json
import os
from datetime import datetime
from src.config import EXPENSES_FILE, DATA_DIR, BUDGETS_FILE, DEFAULT_CATEGORIES
import uuid
import calendar

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
    count = len(data)
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
    expenses = data

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

@tool
def filter_expenses(category: str = None, month: str = None,
                    year: int = None, start_date: str = None,
                    end_date: str = None, min_amount: float = None,
                    max_amount: float = None) -> dict:
    """
    Get a list of filtered expenses using optional filters.
    
    If using a category filter and the category doesn't exist, it will not return the list. So make sure to use correct category
    Categories are = ['food', 'transport', 'entertainment', 'utilities', 'shopping', 'health', 'education', 'other']
    
    Parameters:
    - category (str, optional): Category to filter and get the expenses of (e.g., 'food', 'transport', 'entertainment', 'utilities', 'shopping', 'health', 'education', 'other')
    - month (str, optional) -> "january", "february", etc.
    - year (int, optional) -> 2024, 2025
    - start_date (str, optional) -> format YYYY-MM-DD
    - end_date (str, optional) -> format YYYY-MM-DD
    - min_amount (float, optional)
    - max_amount (float, optional)
    
    Returns:
    - dict: Filtered results formatted as string
    """
    if category is not None and not category.lower() in DEFAULT_CATEGORIES:
        return {"result": f"category doesn't exist {category}"}
    
    expenses = load_expenses()

    filtered_expenses = []
    now = datetime.now()
    
    for exp in expenses:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")

        # Category Filter
        if category:
            if exp["category"].strip().lower() != category.strip().lower():
                continue
        
        # Month Filter
        if month:
            try:
                month_num = list(calendar.month_name).index(month.lower().capitalize())
                if exp_date.month != month_num:
                    continue
            except ValueError:
                continue

        # Year Filter
        if year:
            if exp_date.year != year:
                continue

        # Date Range Filter
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            if exp_date < start:
                continue

        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            if exp_date > end:
                continue

        # Amount Range Filter
        if min_amount is not None:
            if exp["amount"] < min_amount:
                continue
        
        if max_amount is not None:
            if exp["amount"] > max_amount:
                continue
        filtered_expenses.append(exp)
    
    if not filtered_expenses:
        return {"result": "No expenses with passed filters"}
    
    result = f"Found {len(filtered_expenses)} matching expenses:\n\n"

    total = 0
    for i, exp in enumerate(filtered_expenses, 1):
        total += exp["amount"]
        result += (
            f"{i}. [{exp['date']}] "
            f"{exp['category'].upper()} - "
            f"${exp['amount']:.2f}\n"
            f"  Description: {exp['description']}\n\n"
        )
    result += f"Total amount: ${total:.2f}"

    return {"result": result}


@tool 
def remove_expense(category: str = None, amount: float = None,
                   year: int = None, month: str = None) -> dict:
    """
    Removes an expense with given key.
    
    Use this to remove an expense with any of these params (category, amount, year, month)
    Parameters:
    - category (str, optional): -> ('food', 'transport', 'entertainment', 'utilities', 'shopping', 'health', 'education', 'other')
    - amount (float, optional): -> eg. 10.0$, 4$
    - year (int, optional): -> 2025, 2026, etc
    - month (str, optional): -> 'january', 'february', etc
    
    Returns:
    - dict: A confimration message or an error if fails.
    """

    expenses = load_expenses()
    remaining_expenses = []
    removed_count = 0

    for exp in expenses:
        exp_date = datetime.strptime(exp["date"], "%Y-%m-%d")
        match = True

        if category:
            if category.strip().lower() not in DEFAULT_CATEGORIES:
                return {"result": "Error: not a correct category"}
            if exp['category'].strip().lower() != category.strip().lower():
                match = False

        if amount is not None:
            if exp['amount'] != amount:
                match = False

        if year:
            if (exp_date.year != year):
                match = False

        if month:
            try:
                month_num = list(calendar.month_name).index(month.lower().capitalize())
                if (exp_date.month != month_num):
                    match = False
            except ValueError:
                return {"result": "Error: Invalid month."}
        if match:
            removed_count+=1
        else:
            remaining_expenses.append(exp)

    if removed_count == 0:
        return {"result": "No matching expenses found."}
    save_expenses(remaining_expenses)
    return {"result": f"Removed {removed_count} expense(s)."}
    

        
        
