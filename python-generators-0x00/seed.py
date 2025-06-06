import mysql.connector
import csv
import uuid

def connect_db():
    """Connect to MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # عدلها حسب بياناتك
            password="ELHARBA123"           # عدلها حسب بياناتك
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_database(connection):
    """Create ALX_prodev database if not exists."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()

def connect_to_prodev():
    """Connect to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # عدلها حسب بياناتك
            password="",        # عدلها حسب بياناتك
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_table(connection):
    """Create user_data table if not exists."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL,
        UNIQUE(email)
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    """Insert data from CSV to user_data table."""
    cursor = connection.cursor()

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Generate UUID if not in CSV
            user_id = str(uuid.uuid4())

            # Check if email already exists to avoid duplicates
            cursor.execute("SELECT email FROM user_data WHERE email=%s", (row['email'],))
            if cursor.fetchone():
                continue  # Skip if email already exists

            insert_query = """
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(insert_query, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
    cursor.close()

def stream_user_data(connection):
    """Generator to fetch user_data rows one by one."""
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, name, email, age FROM user_data")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()

