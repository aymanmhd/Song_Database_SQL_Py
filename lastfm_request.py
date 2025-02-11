import requests

def fetch_track_info():
    API_KEY = '4bf9b151ce4a03a997c8bdcbd5934ab4'
    API_URL = 'https://ws.audioscrobbler.com/2.0/'

    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'format': 'json',
        'limit': 100
    }

    response = requests.get(API_URL, params=params)
    
    if response.status_code != 200:
        print(f"Error: Unable to fetch data from Last.fm. Status Code: {response.status_code}")
        return []

    data = response.json()
    top_tracks = data.get('tracks', {}).get('track', [])
    
    track_info_list = []

    for index, track in enumerate(top_tracks):
        title = track['name']
        artist_name = track['artist']['name']
        
        track_params = {
            'method': 'track.getInfo',
            'api_key': API_KEY,
            'format': 'json',
            'artist': artist_name,
            'track': title
        }
        
        track_response = requests.get(API_URL, params=track_params)
        
        if track_response.status_code != 200:
            print(f"Error: Unable to fetch track info for {title} by {artist_name}. Status Code: {track_response.status_code}")
            continue
        
        track_data = track_response.json()
        
        album_name = track_data.get('track', {}).get('album', {}).get('title', 'Single')
        genre = track_data.get('track', {}).get('toptags', {}).get('tag', [{}])[0].get('name', 'N/A')

        if genre == "MySpotigramBot": # Defaults to this if no value is found
            genre = "N/A"

        stream_count = track_data.get('track', {}).get('playcount', 'N/A')
        lastfm_url = track_data.get('track', {}).get('url', 'N/A')

        track_info_list.append({
            "rank": index + 1,
            "title": title,
            "artist_name": artist_name,
            "album_name": album_name,
            "genre": genre,
            "stream_count": stream_count,
            "lastfm_url": lastfm_url
        })
    
    return track_info_list

if __name__ == "__main__":
    track_info = fetch_track_info()
    for info in track_info:
        print(info)
