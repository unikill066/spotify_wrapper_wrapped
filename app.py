# imports
import os, spotipy, streamlit as st, pandas as pd
from collections import Counter
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
# local imports
from song_analysis import SongAnalyzer
load_dotenv()  # load environment variables from .env file

SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_CLIENT_ID"), os.getenv("SPOTIPY_CLIENT_SECRET"), os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                              client_secret=SPOTIPY_CLIENT_SECRET,
                              redirect_uri=SPOTIPY_REDIRECT_URI,
                              scope="user-top-read user-read-recently-played user-read-private user-library-read")
                              # add all the necessary permissions here using *scopy*
)


st.set_page_config(page_title="Spotify Wrapped 🎶", page_icon="🎵", layout="wide")

st.sidebar.title("🎛️ Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["short_term", "medium_term", "long_term"],
    format_func=lambda x: {
        "short_term": "Last 4 Weeks",
        "medium_term": "Last 6 Months",
        "long_term": "All Time"
    }[x]
)

# more on caching : https://docs.streamlit.io/get-started/fundamentals/advanced-concepts
# caching allows your app to stay performant even when loading data from the web, manipulating large datasets, or performing expensive computations.

@st.cache_data
def fetch_top_tracks(time_range):
    results = sp.current_user_top_tracks(limit=20, time_range=time_range)
    data = []
    for item in results['items']:
        data.append({
            "Track ID": item['id'],
            "Track Name": item['name'],
            "Artist": item['artists'][0]['name'],
            "Popularity": item['popularity'],
            "Album": item['album']['name'],
            "Image": item['album']['images'][0]['url'] if item['album']['images'] else None,
            "Preview URL": item.get('preview_url')  # <-- Optional, might be useful later
        })
    return pd.DataFrame(data)

@st.cache_data
def fetch_top_artists(time_range):
    results = sp.current_user_top_artists(limit=20, time_range=time_range)
    data = []
    for item in results['items']:
        data.append({
            "Artist Name": item['name'],
            "Genres": ", ".join(item['genres']),
            "Popularity": item['popularity'],
            "Image": item['images'][0]['url'] if item['images'] else None
        })
    return pd.DataFrame(data)

tracks_df = fetch_top_tracks(time_range)
artists_df = fetch_top_artists(time_range)

st.title("Spotify Unwrapped")
st.write(f"Analyzing your Spotify data over **{time_range.replace('_', ' ')}**")

st.subheader("Your Top Genres")
all_genres = []
for genres in artists_df['Genres']:
    all_genres.extend([genre.strip() for genre in genres.split(",")])

genre_counts = Counter(all_genres)
genre_df = pd.DataFrame(genre_counts.items(), columns=['Genre', 'Count']).sort_values(by="Count", ascending=False)

st.bar_chart(genre_df.set_index('Genre'))

st.subheader("Your Music Taste")
result = SongAnalyzer().analyze(tracks_df, artists_df)
st.write(result)

view_option = st.selectbox(
    "Choose what you want to see:",
    options=["Top Tracks", "Top Artists"],
    index=0
)
st.subheader(" ")

def render_grid(df, is_tracks=True):
    rows = (len(df) + 4) // 5
    for row in range(rows):
        cols = st.columns(5)
        for i in range(5):
            idx = row * 5 + i
            if idx < len(df):
                item = df.iloc[idx]
                with cols[i]:
                    if item.get('Image'):
                        st.image(item['Image'], width=300)
                    
                    if is_tracks:
                        st.markdown(f"**{item['Track Name']}**")
                        st.markdown(f"*{item['Artist']}*")
                    else:
                        st.markdown(f"**{item['Artist Name']}**")
                        st.markdown(f"*Genres:* {item['Genres']}")
                    
                    st.markdown(f"(Popularity: {item['Popularity']})")
                    st.markdown("---")

if view_option == "Top Artists":
    st.subheader("🎤 Your Top Artists")
    render_grid(artists_df, is_tracks=False)
elif view_option == "Top Tracks":
    st.subheader("🔥 Your Top Tracks")
    render_grid(tracks_df, is_tracks=True)


st.sidebar.subheader("⬇️ Download Your Data")
csv_tracks = tracks_df.to_csv(index=False).encode('utf-8')
csv_artists = artists_df.to_csv(index=False).encode('utf-8')

st.sidebar.download_button(
    label="Download Top Tracks CSV",
    data=csv_tracks,
    file_name="top_tracks.csv",
    mime="text/csv",
)

st.sidebar.download_button(
    label="Download Top Artists CSV",
    data=csv_artists,
    file_name="top_artists.csv",
    mime="text/csv",
)