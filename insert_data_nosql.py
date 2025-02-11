from neo4j import GraphDatabase

URI = "neo4j+s://e0680b3a.databases.neo4j.io"
AUTH = ("neo4j", "_F22z82A65bPJu-iTqXCBblXi0qFhL0vkAy4MFQloe0")

def get_max_song_id(driver):
    with driver.session() as session:
        result = session.run("MATCH (s:Song) RETURN COALESCE(MAX(toInteger(s.songId)), 0) AS maxId") #  Same as AUTO-INCREMENT on song_id in SQL
        return result.single()["maxId"]

def insert_spotify_tracks(driver, spotify_tracks):
    max_song_id = get_max_song_id(driver)
    with driver.session() as session:
        for index, track in enumerate(spotify_tracks, start=1):
            song_id = max_song_id + index
            track["songId"] = str(song_id)
            session.run(
                """
                CREATE (:Song {
                    songId: $songId,
                    title: $title,
                    artist: $artist_name,
                    album: $album_name,
                    releaseDate: $release_date,
                    genre: $genre,
                    popularityScore: $popularity_score,
                    spotifyUrl: $spotify_url
                })
                """,
                track
            )

def insert_lastfm_tracks(driver, lastfm_tracks):
    max_song_id = get_max_song_id(driver)
    with driver.session() as session:
        for index, track in enumerate(lastfm_tracks, start=1):
            song_id = max_song_id + index
            track["songId"] = str(song_id)
            session.run(
                """
                CREATE (:Song {
                    songId: $songId,
                    title: $title,
                    artist: $artist_name,
                    album: $album_name,
                    genre: $genre,
                    streamCount: $stream_count,
                    lastFmUrl: $lastfm_url
                })
                """,
                track
            )

if __name__ == "__main__":
    from spotify_request import fetch_track_info as fetch_spotify_tracks
    from lastfm_request import fetch_track_info as fetch_lastfm_tracks


    spotify_playlist_id = '2YVULLKXdUsPCOqzws1LCP' # TODO: CHANGE TO CORRECT PLAYLIST (DIDN'T WORK FOR ME FOR SOME REASON)
    spotify_tracks = fetch_spotify_tracks(spotify_playlist_id)
    lastfm_tracks = fetch_lastfm_tracks()

    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        insert_spotify_tracks(driver, spotify_tracks)
        insert_lastfm_tracks(driver, lastfm_tracks)
