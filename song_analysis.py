"""
Song Analysis is a class that uses OpenAI's GPT-3.5-turbo model to analyze a user's top songs and artists.

Created by **Inturi, Nikhil Nageshwar**

Licensed under the **MIT License**
"""

# imports
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from prompt_template import *

load_dotenv()  # load environment variables from .env file

class SongAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")

    def generate_prompt(self, tracks: pd.DataFrame, artists: pd.DataFrame):
        top_songs_str = "\n".join(
            [f"Song: {row[TRACK_NAME]} – Artist: {row[ARTIST]} - Popularity: {row[POPULARITY]} - Album: {row[ALBUM]}" 
             for _, row in tracks.iterrows()])
        top_artists_str = "\n".join(
            [f"Artist: {row[ARTIST_NAME]} – Genres: {row[GENRES] if pd.notna(row[GENRES]) else 'N/A'} – Popularity: {row[POPULARITY]}" 
             for _, row in artists.iterrows()])
        
        prompt = music_analysis_prompt.format(top_songs=top_songs_str, top_artists=top_artists_str)
        return prompt
    
    def analyze(self, tracks: pd.DataFrame, artists: pd.DataFrame):
        prompt = self.generate_prompt(tracks, artists)
        return self.llm.invoke(prompt).content