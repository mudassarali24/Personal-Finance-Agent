from langchain.tools import tool
import json
import os
from datetime import datetime
from src.config import EXPENSES_FILE, DATA_DIR

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
def get_expenses_count() -> dict:
    """Get the total numnber of expenses recorded.
    
    Returns:
    - dict: A dictionary with the total count of expenses."""
    data = load_expenses()
    count = 0
    count = len(data.get("expenses", []))
    return {"result": count}