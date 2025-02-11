from spotify_request import fetch_track_info as fetch_spotify_data  # Import Spotify data fetch function
from lastfm_request import fetch_track_info as fetch_lastfm_data    # Import Last.fm data fetch function
import psycopg2

# Function to create a database connection
def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="MusicStreamingDB",
            user="postgres",  
            password="postgres",
            host="localhost" 
        )
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Function to insert Spotify data
def insert_spotify_data(connection, track_data):
    try:
        with connection.cursor() as cursor:
            for track in track_data:
                # Insert into Songs table
                cursor.execute('''
                    INSERT INTO Songs (rank, title, artist, album, release_date, genre)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING song_id;
                ''', (
                    track["rank"], 
                    track["title"], 
                    track["artist_name"], 
                    track["album_name"], 
                    track["release_date"], 
                    track["genre"]
                ))
                
                song_id = cursor.fetchone()[0]  # Get the generated song_id

                # Insert into SpotifySongs table
                cursor.execute('''
                    INSERT INTO SpotifySongs (song_id, spotify_popularity_score, spotify_url)
                    VALUES (%s, %s, %s);
                ''', (
                    song_id, 
                    track["popularity_score"], 
                    track["spotify_url"]
                ))

            connection.commit()
            print("Spotify data inserted successfully!")
    except Exception as e:
        connection.rollback()
        print("Error inserting Spotify data:", e)

# Function to insert Last.fm data
def insert_lastfm_data(connection, track_data):
    try:
        with connection.cursor() as cursor:
            for track in track_data:
                # Insert into Songs table
                cursor.execute('''
                    INSERT INTO Songs (rank, title, artist, album, release_date, genre)
                    VALUES (%s, %s, %s, %s, NULL, %s)
                    RETURNING song_id;
                ''', (
                    track["rank"], 
                    track["title"], 
                    track["artist_name"], 
                    track["album_name"], 
                    track["genre"]
                ))
                
                song_id = cursor.fetchone()[0]  # Get the generated song_id

                # Insert into LastfmSongs table
                cursor.execute('''
                    INSERT INTO LastfmSongs (song_id, lastfm_stream_count, lastfm_url)
                    VALUES (%s, %s, %s);
                ''', (
                    song_id, 
                    track["stream_count"], 
                    track["lastfm_url"]
                ))

                cursor.execute(''' 
                    UPDATE Songs
                    SET genre = NULL
                    WHERE genre = 'N/A';
                ''')

            connection.commit()
            print("Last.fm data inserted successfully!")
    except Exception as e:
        connection.rollback()
        print("Error inserting Last.fm data:", e)

# Main function to fetch data and insert into the database
def main():
    connection = create_connection()
    if connection:
        print("Fetching Spotify data...")
        spotify_data = fetch_spotify_data('37i9dQZEVXbMDoHDwVN2tF')  # Replace with your Spotify playlist ID
        insert_spotify_data(connection, spotify_data)

        print("Fetching Last.fm data...")
        lastfm_data = fetch_lastfm_data()
        insert_lastfm_data(connection, lastfm_data)

        connection.close()  # Close the connection
        print("All data inserted successfully!")

if __name__ == "__main__":
    main()
