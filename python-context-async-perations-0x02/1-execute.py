import sqlite3

# Class-based context manager to execute a query with parameters
class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Open database connection and execute the query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        # Close cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Example usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)

with ExecuteQuery("my_database.db", query, params) as results:
    print(results)

