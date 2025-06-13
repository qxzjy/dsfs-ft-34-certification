# Anime recommendation engine 🏯

Welcome to our Data Science & Engineering fullstack project !

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

<a href="https://marjg-anime-recommendation-engine.hf.space/" target="_blank">Here is the link to the app</a>

### Dependencies

For local use :
* Feel free to use our DockerHub Image : `lyxor/anime-recommendation-engine`
* All needed libraries are in the `requirements.txt` file
* A mistral api key

### Installing and execute

For running the app in local  :
* `git clone https://github.com/qxzjy/anime-recommendation-engine.git`
* go inside anime-recommendation-engine
* add your MISTRAL_API_KEY in your environnement variable or export it : `export MISTRAL_API_KEY=your_key`

With DockerHub image:
* `docker run -p 8501:8501 -v $(pwd):/app -e MISTRAL_API_KEY=$MISTRAL_API_KEY lyxor/anime-recommendation-engine`

With local docker image:
* `docker build . -t your_image_name`
* `docker run -p 8501:8501 -v $(pwd):/app -e MISTRAL_API_KEY=$MISTRAL_API_KEY your_image_name`

## Authors

By [@Marjorie](https://github.com/Marjorie-J), [@Antoine](https://github.com/AntOG96), [@Maxime](https://github.com/qxzjy) and [@Florent](https://github.com/LyXoR51)

## Version History

* 0.1
    * Initial Release