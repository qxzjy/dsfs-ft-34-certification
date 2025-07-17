import streamlit as st

from utils.common import load_animes, load_anime, load_synopsis_embedding, search_closest_by_uid, write_col, write_col_with_label, display_img, display_synopsis, load_hentai_uid

from utils.common import load_animes, load_anime, load_synopsis_embedding, search_closest_by_uid, write_col, write_col_with_label, display_img, display_synopsis, display_review

st.markdown("## 🎥 Anime Search & Similar Recommendations")

st.write(
    """Search for an anime and discover similar titles based on their descriptions.  
This tool helps you find new animes with themes and storylines that match your interests."""
)

# Load data
df_animes = load_animes()
df_emb = load_synopsis_embedding()
df_hentai_uid = load_hentai_uid()

# Create a dictionnary {title to show : id}
if st.session_state['hentai_filter_on'] :
    df_animes =  df_animes[~df_animes['uid'].isin(df_hentai_uid)]

animes_dict = {row["title"]: row["uid"] for _, row in df_animes.iterrows()}

# SelectBox
selected_anime_uid = st.selectbox("Choose anime",
    animes_dict,
    index=None,
    placeholder="Select an anime ...")

# Anime selected
if selected_anime_uid != None :

    selected_anime = load_anime(df_animes, animes_dict[selected_anime_uid])

    if selected_anime is not None:

        # Anime informations
        container = st.container(border=True)
        container.write("Anime informations")
        col1, col2 = container.columns(2)
        with col1:
            display_img(selected_anime["img_url"], selected_anime["title"])
        with col2:
            write_col(selected_anime["synopsis"])
            write_col_with_label(selected_anime["episodes"], "Episodes : ")
            if st.button(label="Reviews' summary"):
                display_review(selected_anime["uid"])


        # RECO_01
        with st.expander("Anime recommendations based on the description"):
            
            if selected_anime["synopsis"] is None or selected_anime["synopsis"] != selected_anime["synopsis"]:
                st.write("No recommendation provided, the synopsis is missing.")
            else:
                closest_anime_synopsis = search_closest_by_uid(selected_anime["uid"], df_emb)
                
                favorites_anime = closest_anime_synopsis['uid'].tolist()

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