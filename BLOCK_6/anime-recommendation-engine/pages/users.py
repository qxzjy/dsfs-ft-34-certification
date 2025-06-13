import ast
import streamlit as st

from utils.common import load_profiles, load_profile, load_animes, load_anime, load_als_favorite_recommendations, load_profile_recommendations, load_als_reviews_recommendations, display_synopsis, load_hentai_uid, display_img

st.markdown("## 🥷 User-Based Anime Recommendations")

st.write(
    """Discover anime recommendations tailored to your viewing history and preferences.  
We analyze your liked animes and compare them with other users favorites to suggest titles you might enjoy."""
)

# Load data
df_als_favorite_recommendation = load_als_favorite_recommendations()
df_als_reviews_recommendation = load_als_reviews_recommendations()
df_animes = load_animes()
df_profiles = load_profiles()
df_hentai_uid = load_hentai_uid()

# SelectBox
selected_user_profile = st.selectbox("Choose user",
    df_profiles["profile"],
    index=None,
    placeholder="Select a user ...")

# Anime selected
if selected_user_profile != None :
    selected_profile = load_profile(df_profiles, selected_user_profile)
    selected_profile_favorite_recommendations = load_profile_recommendations(df_als_favorite_recommendation, selected_user_profile)
    selected_profile_reviews_recommendations = load_profile_recommendations(df_als_reviews_recommendation, selected_user_profile)

    # Favorite anims
    with st.expander("Favorite anims"):
        favorites_anime = ast.literal_eval(selected_profile["favorites_anime"]) # Update HERE to exclude Hentai

        if st.session_state['hentai_filter_on'] :
                    favorites_anime =  [value for value in favorites_anime if value not in df_hentai_uid.tolist()]

        if favorites_anime:
            for i in range(0, len(favorites_anime), 3):
                cols = st.columns(3)
                for col, fav in zip(cols, favorites_anime[i:i+3]):
                    anime = load_anime(df_animes, fav)
                    if anime is not None:
                        with col:
                            display_img(anime["img_url"])
                            if st.button(label=anime["title"]):
                                display_synopsis(anime)
        else:
            st.write("No favorite anime to display.")

    # RECO_02
    with st.expander("Anime recommendations based on what users who liked the same things as me"):

        if selected_profile_favorite_recommendations.empty :
                st.write("No recommendation provided, no favorites animes.")
        else:
            recommendations = ast.literal_eval(selected_profile_favorite_recommendations["recommendations"])

            if st.session_state['hentai_filter_on'] :
                recommendations = [value for value in recommendations if value not in df_hentai_uid.tolist()]
             
            recommendations = recommendations[:5]
          
            for i in range(0, len(recommendations), 3):
                cols = st.columns(3)
                for col, fav in zip(cols, recommendations[i:i+3]):
                    anime = load_anime(df_animes, fav)
                    if anime is not None:
                        with col:
                            display_img(anime["img_url"])
                            if st.button(label=anime["title"]):
                                display_synopsis(anime) 

    # RECO_03
    with st.expander("Anime recommendations based on my review scores"):

        if selected_profile_reviews_recommendations.empty :
                st.write("No recommendation provided, no favorites animes.")
        else:
            recommendations = ast.literal_eval(selected_profile_reviews_recommendations["recommendations"])

            if st.session_state['hentai_filter_on'] :
                recommendations = [value for value in recommendations if value not in df_hentai_uid.tolist()]

            recommendations = recommendations[:5]    

            for i in range(0, len(recommendations), 3):
                cols = st.columns(3)
                for col, fav in zip(cols, recommendations[i:i+3]):
                    anime = load_anime(df_animes, fav)
                    if anime is not None:
                        with col:
                            display_img(anime["img_url"])
                            if st.button(label=anime["title"]):
                                display_synopsis(anime)