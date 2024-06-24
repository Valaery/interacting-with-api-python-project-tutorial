import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from textwrap import wrap

# Load the .env file variables
load_dotenv()

# Artist URI
DQ_URI = 'spotify:artist:5AWgF8Ghqm94WZ4GxCt8K5'

# Get Spotify API credentials from environment variables
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

# Authenticate with Spotify API
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

try:
    results = spotify.artist_top_tracks(DQ_URI)
    
    # Check if the response contains tracks
    if 'tracks' not in results or not results['tracks']:
        raise ValueError("No tracks found for the given artist URI.")

    # Extract the relevant information and convert to DataFrame
    tracks = results['tracks']
    tracks_data = [{
        'name': track['name'],
        'popularity': track['popularity'],
        'album': track['album']['name'],
        'release_date': track['album']['release_date'],
        'track_url': track['external_urls']['spotify']
    } for track in tracks]

    df = pd.DataFrame(tracks_data)
    
    # Wrap long track names for better visibility
    df['wrapped_name'] = df['name'].apply(lambda x: '\n'.join(wrap(x, 30)))

    # Plotting the popularity of tracks
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='popularity', y='wrapped_name', dodge=False, palette='viridis')
    plt.title('Popularity of Top Tracks')
    plt.xlabel('Popularity')
    plt.ylabel('Track Name')
    plt.tight_layout()
    plt.savefig('./img/popularity_of_top_tracks.png')
    
    plt.show()
    
except spotipy.SpotifyException as e:
    print(f"Spotify API error: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
