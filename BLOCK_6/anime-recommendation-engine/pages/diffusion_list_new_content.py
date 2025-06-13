import streamlit as st

from utils.common import generate_diffusion_list, load_animes, extract_animes_from_uid, load_profiles

# Load data
df_animes = load_animes()
df_profiles = load_profiles()

st.markdown("## 💻 Diffusion list for new content")

st.write(
    """ List of diffusions for new content, based on the synopsis and targeting profiles who have favorited similar content. """
)


# Form
with st.form("anime_input_form"):
    input_anime_description = st.text_area("Summit the new content synopsis to generate the diffusions list !")
    submitted = st.form_submit_button("Find")

    # Update HERE to exclude Hentai ?!

    if submitted:
        diffusion_list_df = generate_diffusion_list(input_anime_description)

        st.write("#### Because they loved:")
        
        selected_animes = extract_animes_from_uid(df_animes, diffusion_list_df)

        st.write(selected_animes[['title','uid']])

        st.write(f"#### Profiles found: {diffusion_list_df.shape[0]}    ({round(diffusion_list_df.shape[0]/df_profiles.shape[0],3)*100}% of all profiles)")
        st.write(diffusion_list_df['profile'])