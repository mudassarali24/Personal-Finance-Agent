# Personal Finance Agent

An AI-powered personal finance assistant that helps you track expenses and manage budgets.

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Create `.env` file with your API key:
```
   GROQ_API_KEY=your_key_here
```
5. Run the agent:
```bash
   python main.py
```

## Features

- [x] Basic agent setup
- [ ] Track expenses
- [ ] View spending by category
- [ ] Set and monitor budgets
- [ ] Spending trends and insights

## Project Structure
```
personal-finance-agent/
├── src/
│   ├── agent.py      # Agent setup
│   ├── tools.py      # Tool definitions
│   ├── prompts.py    # System prompts
│   └── config.py     # Configuration
├── data/             # Expense data storage
├── main.py           # Entry point
└── requirements.txt  # Dependencies
```