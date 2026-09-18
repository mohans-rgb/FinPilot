

from fastmcp import FastMCP
from . import services
from . import flights
from .settings import settings
from .database import init_db

mcp = FastMCP(name="FinPilot")


@mcp.tool
def add_expense(amount:float, category:str, note:str = "", spent_on:str = "") -> str:
    """
        Record a new expense.
        
        Args:
            amount: how much was spent (e.g. 12.50)
            category: a category like 'food', 'rent', 'transport'
            note: optional descriptiopn
            spent_on: optional date 'YYYY-MM-DD' (default to today)
    """
    
    return services.add_expense(amount, category, note, spent_on)
    
    
@mcp.tool
def list_expenses(month:str = "", category:str = "") -> str: 
    """
        List expenses for a month (default current). Optionally filter by category.
        Args:
            month: 'YYYY-MM' (empty = current month)
            category: optional category filter like 'food', 'rent', 'transport'
    """
    return services.list_expenses(month, category)
    


@mcp.tool
def delete_expense(expense_id:int = 0):
    """
    Delete one expense by its id
    """
    return services.delete_expense(expense_id)
    
    
@mcp.tool
def search_flights(from_city:str, to_city:str, travel_date:str = ""):
    """
      Search for available flights between two cities.

    Use this tool when the user wants to find or compare flights
    between an origin and destination city.

    Args:
        from_city: The departure/origin city, e.g. "Delhi".
        to_city: The arrival/destination city, e.g. "Mumbai".
        travel_date: Optional travel date in YYYY-MM-DD format.
                     If omitted, search for flights without restricting
                     the results to a specific date.

    Returns:
        A list of available flights matching the specified route and,
        if provided, travel date.
    """
    return flights.search_flights(from_city, to_city, travel_date)
    
    
if __name__ == "__main__":
    init_db()
    if settings.MCP_TRANSPORT == "http":
        mcp.run(transport="streamable-http", host= settings.MCP_HOST, port = settings.MCP_PORT)
    else:
        mcp.run(transport="stdio")
        