import json
from neo4j import GraphDatabase

# Function to load JSON data from a text file
def load_json_data(filepath):
    with open(filepath, 'r') as file:
        data = json.load(file)
    return data

# Function to create a song node in the database
def create_song_node(driver, rank, title, artist_name, release_date, album_name, genre, popularity_score, spotify_url):
    with driver.session() as session:
        cypher_query = """
        CREATE (:Song {
            rank: $rank,
            title: $title,
            artist: $artist_name,
            releaseDate: $release_date,
            album: $album_name,
            genre: $genre,
            popularityScore: $popularity_score,
            spotifyUrl: $spotify_url
        })
        """
        session.run(cypher_query, rank=rank, title=title, artist_name=artist_name, release_date=release_date,
                    album_name=album_name, genre=genre, popularity_score=popularity_score, spotify_url=spotify_url)

# Function to extract and process each track
def process_tracks(data, driver):
    for index, item in enumerate(data['items']):
        track = item['track']
        title = track['name']
        artist_name = ", ".join([artist['name'] for artist in track['artists']])
        release_date = track['album']['release_date']
        album_name = track['album']['name']
        spotify_url = track['external_urls']['spotify']
        popularity_score = track.get('popularity', 0)  # defaulting to 0 if popularity isn't provided
        
        # Assume only one artist per track for simplicity in accessing genres
        artist_id = track['artists'][0]['id']
        genre = ", ".join(track['artists'][0].get('genres', []))  # Assuming genre data is included in the 'artists' section
        
        create_song_node(driver, index + 1, title, artist_name, release_date, album_name, genre, popularity_score, spotify_url)

# Main function to initiate the process
def main(txt_filepath, uri, user, password):
    data = load_json_data(txt_filepath)
    driver = GraphDatabase.driver(uri, auth=(user, password))
    process_tracks(data, driver)
    driver.close()

# Execute the script with your file path and Neo4j credentials
main('SpotifySongs12.txt', 'neo4j+s://e0680b3a.databases.neo4j.io', 'neo4j', '_F22z82A65bPJu-iTqXCBblXi0qFhL0vkAy4MFQloe0')

