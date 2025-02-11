import psycopg2
from psycopg2 import sql

# Function to create a database connection
def create_connection(dbname, user, password, host):
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host
        )
        return connection
    except Exception as e:
        print(f"Error connecting to the {dbname} database:", e)
        return None

# Function to create the SpotifyAppleMusicDB
def create_database():
    # Insert your  credentials
    connection = create_connection("MusicStreamingDB", "postgres", "postgres", "localhost")
    if connection:
        try:
            connection.autocommit = True  # Enable autocommit mode

            with connection.cursor() as cursor:
                cursor.execute(sql.SQL("CREATE DATABASE MusicStreamingDB;"))
                print("Database 'MusicStreamingDB' created successfully!")

        except Exception as e:
            print("Error creating the database:", e)

        finally:
            connection.close()  # Close the connection to 'postgres'

# Main function to run the script
def main():
    create_database()  # Create the database 

if __name__ == "__main__":
    main()
