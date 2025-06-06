#!/usr/bin/python3

seed = __import__('seed')

def main():
    connection = seed.connect_db()
    if connection:
        print("Connected to MySQL server.")
        seed.create_database(connection)
        connection.close()

        connection = seed.connect_to_prodev()
        if connection:
            print("Connected to ALX_prodev database.")
            seed.create_table(connection)
            seed.insert_data(connection, 'user_data.csv')

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM user_data LIMIT 5;")
            rows = cursor.fetchall()
            print("First 5 rows from user_data:")
            for row in rows:
                print(row)
            cursor.close()
            connection.close()
        else:
            print("Failed to connect to ALX_prodev database.")
    else:
        print("Failed to connect to MySQL server.")

if __name__ == "__main__":
    main()

