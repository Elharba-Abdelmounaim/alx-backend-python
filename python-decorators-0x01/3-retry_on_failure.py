import sqlite3
import functools
import time

# Decorator to handle database connection setup and teardown
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("my_database.db")  # Adjust database name as needed
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Decorator to retry a function on failure due to exceptions
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempts + 1} failed with error: {e}")
                    attempts += 1
                    if attempts < retries:
                        time.sleep(delay)
            # Final attempt, let exception raise if it fails
            return func(*args, **kwargs)
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)

