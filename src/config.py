import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0

DATA_DIR = "data"
EXPENSES_FILE = os.path.join(DATA_DIR, "expenses.json")
BUDGETS_FILE = os.path.join(DATA_DIR, "budgets.json")

DEFAULT_CATEGORIES = [
    "food",
    "transport",
    "entertainment",
    "utilities",
    "shopping",
    "health",
    "education",
    "other"
]