from langchain.prompts import PromptTemplate

music_analysis_prompt = PromptTemplate(
    input_variables=["top_songs", "top_artists"],
    template="""🎧 **Deep Music Taste Analysis (Lyrical + Emotional + Psychological)**

Analyze the user's music taste using their top songs and artists. Focus on lyrical content, emotional tone, and psychological resonance.

---
**Top Songs (Title – Artist – Popularity – Album):**  
{top_songs}

**Top Artists (Name – Genre – Popularity):**  
{top_artists}
---

**Instructions:**

1. **Song Classification: Lyric-Driven vs. Production-Focused**
   - List each song under one of these two categories.
   - For each song, provide a 2-3 sentence analysis: summarize lyrical themes, emotional tone, and any notable artistic or production elements.

2. **Thematic Groupings & Emotional Tone**
   - Group songs into categories (e.g., Heartbreak, Empowerment, Introspection, Production-Driven).
   - For each group, briefly describe the common emotional or thematic thread.

3. **Psychological & Personality Insights**
   - Based on the above, infer possible psychological traits, emotional needs, and personality characteristics.

4. **Overall Musical Identity**
   - Summarize what this music taste suggests about the user's values and emotional world.

**Format your answer using clear section headers, bullet points, and concise language.**
"""
)

TRACK_NAME = "Track Name"
POPULARITY = "Popularity"
ARTIST = "Artist"
ALBUM = "Album"
GENRES = "Genres"
ARTIST_NAME = "Artist Name"
