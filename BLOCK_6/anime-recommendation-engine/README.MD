# Anime recommendation engine 🏯

## Description

This app provides personalized anime recommendations using three main approaches:

- **User-based filtering**: Suggestions are based on what you've watched, liked, and commented on, as well as the preferences of similar users.  
- **Content-based filtering**: Recommendations are made by analyzing the content of anime descriptions to find similar titles.

- **Describe filtering**:  "Tell us what you want — or don’t want — and we’ll recommend the perfect anime !"

Also in the app :

- **EDA**: An analysis of the <a href="https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews" target="_blank">Anime dataset found on Kaggle</a>

- **Review summarization**: An AI generated review based on all users's reviews

- **Diffusion list for new content**: A generated list of users based on the new synopsis and their favorite animes

Enjoy discovering new anime tailored to your tastes!

## Getting Started

<a href="https://qxzjy-streamlit-anime-recommandation-engine.hf.space/" target="_blank">Here is the link to the app</a>

### Run application

To deploy the app locally  :
1. Clone the repository :\
`$ git clone https://github.com/qxzjy/anime-recommendation-engine.git`
2. Go to the repository :\
`$ cd anime-recommendation-engine`
3. Add your MISTRAL_API_KEY in your environnement variable :\
`$ export MISTRAL_API_KEY=your_key`
4. Launch the steamlit app :\
`$ streamlit run app.py`

To deploy the app with DockerHub image :\
`$ docker run -p 8501:8501 -v $(pwd):/app -e MISTRAL_API_KEY=$MISTRAL_API_KEY lyxor/anime-recommendation-engine`

## Authors

[Maxime RENAULT](https://github.com/qxzjy)\
[Marjorie JANDA](https://github.com/Marjorie-J)\
[Antoine OGER](https://github.com/AntOG96)\
[Florent PROUST](https://github.com/LyXoR51)