import sqlite3
import functools

def log_queries():
    # This is the decorator factory that returns the actual decorator
    def decorator(func):
        @functools.wraps(func)  # Preserve metadata of the original function
        def wrapper(*args, **kwargs):
            # Assume the SQL query is passed as a keyword argument named 'query'
            query = kwargs.get('query', None)
            if query:
                print(f"Executing query: {query}")
            else:
                # If not found in kwargs, check if query is passed as first positional argument
                if len(args) > 0:
                    print(f"Executing query: {args[0]}")
            # Call the original function with all arguments
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()  # Apply the decorator to the function
def fetch_all_users(query):
    # Connect to the SQLite database
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Execute the provided SQL query
    cursor.execute(query)
    # Fetch all results from the executed query
    results = cursor.fetchall()
    # Close the database connection
    conn.close()
    # Return the fetched results
    return results

# Example call that triggers the logging of the SQL query
users = fetch_all_users(query="SELECT * FROM users")

