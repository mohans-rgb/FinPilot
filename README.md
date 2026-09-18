# FinPilot — Personal Finance & Travel MCP Server

An [MCP](https://modelcontextprotocol.io) server that exposes personal expense-tracking
and flight-search tools to any MCP-compatible client (Claude Desktop, an
LLM agent, etc.), built with [FastMCP](https://gofastmcp.com).

## What it does

- **Expense tracking** — log, list, and delete personal expenses backed by a
  SQL database (SQLAlchemy).
- **Flight search** — search real-time flight options via SerpAPI's Google
  Flights engine.

## Tools exposed

| Tool | Description |
|---|---|
| `add_expense(amount, category, note, spent_on)` | Record a new expense |
| `list_expenses(month, category)` | List expenses, optionally filtered by month/category |
| `delete_expense(expense_id)` | Delete an expense by ID |
| `search_flights(origin, destination, date)` | Search flights between two cities on a given date |

## Tech stack

Python, FastMCP, SQLAlchemy, SerpAPI, OpenAI

## Setup

1. Clone the repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root :
   ```env
   DATABASE_URL=sqlite:///./finpilot.db
   OPENAI_API_KEY=your_openai_key
   SERPAPI_KEY=your_serpapi_key
   LLM_MODEL=gpt-5
   MCP_TRANSPORT=stdio
   MCP_HOST=0.0.0.0
   MCP_PORT=8000
   ```

3. Run the server:
   ```bash
   python -m FinPilot.main
   ```
