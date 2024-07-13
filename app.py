import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import requests

# Authenticate with Spotify API
client_id = '237ece64a4da4395866b7a4e875a9184'
client_secret = '98389064e25a48ed8815f135c4a44b48'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to recommend music using Spotify API and retrieve album art URLs
def recommend_music(selected_music_name):
    results = sp.search(q=selected_music_name, limit=1)
    if results['tracks']['items']:
        seed_track_id = results['tracks']['items'][0]['id']
        recommendations = sp.recommendations(seed_tracks=[seed_track_id], limit=5)
        recommended_tracks = []
        for track in recommendations['tracks']:
            recommended_tracks.append({
                'name': track['name'],
                'poster': track['album']['images'][0]['url'] if track['album']['images'] else None
            })
        return recommended_tracks
    else:
        return []

music = pd.read_csv(r'/Users/soham/Documents/MINI_PROJECTS/Music_Recomender/ex.csv')

# Streamlit app
st.title('Music Recommendation System')

selected_music_name = st.selectbox('Select a music you like', music['Song-Name'].values)

if st.button('Recommend'):
    recommended_music = recommend_music(selected_music_name)

    if recommended_music:
        st.write('Recommended Music:')
        col1, col2, col3, col4, col5 = st.columns(5)  # Divide into 5 columns

        for i, track in enumerate(recommended_music):
            with col1 if i % 5 == 0 else col2 if i % 5 == 1 else col3 if i % 5 == 2 else col4 if i % 5 == 3 else col5:
                st.text(f"{i+1}. {track['name']}")
                if track['poster']:
                    st.image(track['poster'], width=150, ) 
                    
                else:
                    st.write("No poster available.")
    else:
        st.write('No recommendations found.')
