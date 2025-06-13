import streamlit as st

from utils.common import load_animes, load_profiles, load_reviews, load_synopsis_embedding,  init_model_MiniLM

st.title("Anime Recommendation Engine 🏯")

st.markdown("""
## Welcome to the Anime Recommendation System!

This app provides personalized anime recommendations using two main approaches:

- **User-based filtering**: Suggestions are based on what you've watched, liked, and commented on, as well as the preferences of similar users.  
- **Content-based filtering**: Recommendations are made by analyzing the content of anime descriptions to find similar titles.  

Enjoy discovering new anime tailored to your tastes!
""")