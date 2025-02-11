import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def fetch_track_info(playlist_id):
    client_id = '9ccfa603b1e44e4d83df5e07d118dcc8'
    client_secret = '95f173867e00467991ca93235f4c1ed8'
    
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    tracks_data = sp.playlist_tracks(playlist_id=playlist_id, limit=101)
    
    track_info_list = []
    for index, item in enumerate(tracks_data['items']):
        track = item['track']
        title = track['name']
        artist_name = ", ".join([artist['name'] for artist in track['artists']])
        release_date = track['album']['release_date']
        album_name = track['album']['name']
        spotify_url = track['external_urls']['spotify']
        popularity_score = track['popularity']
        
        artist_id = track['artists'][0]['id']
        artist_data = sp.artist(artist_id)
        genre = ", ".join(artist_data.get('genres', []))
        
        track_info_list.append({
            "rank": index + 1,  # rank is the index + 1
            "title": title,
            "artist_name": artist_name,
            "release_date": release_date,
            "album_name": album_name,
            "genre": genre,
            "popularity_score": popularity_score,
            "spotify_url": spotify_url
        })
    
    return track_info_list

if __name__ == "__main__":
    playlist_id = '2wXG9S1idTQQwheVfsS6ZV'
    track_info = fetch_track_info(playlist_id)
    for info in track_info:
        print(info)

