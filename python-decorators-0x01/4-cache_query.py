import time
import sqlite3
import functools

# Dictionary to store cached query results
query_cache = {}

# Decorator to manage database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")  # Use the actual database file
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Decorator to cache query results to avoid redundant DB calls
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already cached
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        # Otherwise, execute and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print("First fetch:", users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print("Second fetch (cached):", users_again)

