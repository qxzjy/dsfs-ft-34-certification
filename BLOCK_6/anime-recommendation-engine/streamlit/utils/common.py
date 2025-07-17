from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import Optional

import re
import streamlit as st
import pandas as pd
import ast
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # remonte à la racine du projet

DATA_ANIMES_URL = os.path.join(BASE_DIR, "datas", "animes_clean.csv")
DATA_PROFILES_URL = os.path.join(BASE_DIR, "datas", "profiles_clean.csv")
DATA_REVIEWS_URL = os.path.join(BASE_DIR, "datas", "reviews_clean.csv")
DATA_SYNOPSIS_EMBEDDING_URL = os.path.join(BASE_DIR, "datas", "synopsis_embedding.json")
DATA_ALS_RECOMMENDATION_FAVORITE_URL = os.path.join(BASE_DIR, "datas", "als_is_favorite_based_reco.csv")
DATA_ALS_RECOMMENDATION_REVIEWS_URL = os.path.join(BASE_DIR, "datas", "als_reviews_score_based_reco.csv")

# ANIMES
@st.cache_data
def load_animes(nrows=None):
    data = pd.read_csv(DATA_ANIMES_URL, nrows=nrows)
    data["episodes"] = data["episodes"].astype("Int64")
    data.sort_values("title", axis=0, ascending=True, inplace=True)
    return data

@st.cache_data
def load_anime(df, uid):
    selected_anime = df[df["uid"]==int(uid)]
    if selected_anime.empty:
        return None
    return selected_anime.iloc[0]

@st.cache_data
def load_hentai_uid():
    data = pd.read_csv(DATA_ANIMES_URL)
    data["genre"] = data["genre"].apply(ast.literal_eval)
    df_hentai = data[["uid", "genre"]].copy().explode("genre")
    df_hentai = df_hentai[df_hentai["genre"]=="Hentai"]
    return df_hentai["uid"]
##


# PROFILES
@st.cache_data
def load_profiles(nrows=None):
    data = pd.read_csv(DATA_PROFILES_URL, nrows=nrows)
    data.sort_values("profile", axis=0, ascending=True, inplace=True)
    return data

@st.cache_data
def load_profile(df, profile):
    selected_profile = df[df["profile"]==profile]
    return selected_profile.iloc[0]
##


# REVIEWS
@st.cache_data
def load_reviews(nrows=None):
    data = pd.read_csv(DATA_REVIEWS_URL, nrows=nrows)
    return data
##

# SYNOPSIS EMBEDDING
@st.cache_data
def load_synopsis_embedding(nrows=None):
    data = pd.read_json(DATA_SYNOPSIS_EMBEDDING_URL, nrows=nrows)
    return data

def closest_similarity(target, df, col_category=None, category=None):
        if col_category:
                mask = df[col_category].apply(lambda lst: category in lst)
                df = df[~mask]
        similarities = cosine_similarity([target], list(df['synopsis_embedding']))[0]
        similarity_df = pd.DataFrame({'uid': df['uid'], 'similarity': similarities})
        similarity_df =  similarity_df.sort_values(by='similarity', ascending=False)

        return similarity_df

def search_closest_by_uid(given_uid, df):     
        given_embedding = df.loc[df['uid'] == given_uid, 'synopsis_embedding'].values[0]
        similarity_df = closest_similarity(given_embedding, df)
        closest = similarity_df[similarity_df['uid'] != given_uid].sort_values(by='similarity', ascending=False).head()
        return closest
##

# NAN
def write_col(col):
    if col is None or col != col:
        st.write("No information available.")
    else:
        st.write(col)

def write_col_with_label(col, label):
    if col is None or pd.isna(col):
        st.write(f"{label}No information available.")
    else:
        st.write(f"{label}{col}")

def display_img(col_image, col_caption=None):
    if col_image is None or col_image != col_image:
        st.write("No picture to display.")
    else:
        st.image(col_image, caption=col_caption, width=300)
##

# ALS (Collaborative filtering)
@st.cache_data
def load_als_favorite_recommendations():
    data = pd.read_csv(DATA_ALS_RECOMMENDATION_FAVORITE_URL)
    return data

@st.cache_data
def load_als_reviews_recommendations():
    data = pd.read_csv(DATA_ALS_RECOMMENDATION_REVIEWS_URL)
    return data

@st.cache_data
def load_profile_recommendations(df, profile):
    selected_profile = df[df["profile"]==profile]
    if selected_profile.empty :
        return selected_profile
    return selected_profile.iloc[0]
##

#cleaning of a text
def clean_text(text):
    text = re.sub("[\n\r]", " ", text)
    text = re.sub("[^A-Za-z0-9]+", " ", text)
    return text

## RECO_05 : input in natural language

# Output format
class OutputSchema_describe(BaseModel):
    positive: str
    negative: str
    title: Optional[str]

class OutputSchema_review(BaseModel):
    positive: str
    negative: str

# init Model LLM
@st.cache_resource
def init_model_llm(sys_prompt):


    # Define system prompt
    start_prompt = ChatPromptTemplate.from_messages([
        ("system", sys_prompt),
        ("user", "{text}")
    ])

    # Don't forget your API Key : export MISTRAL_API_KEY=...

    # Let's instanciate a model 
    llm = ChatMistralAI(model="mistral-medium-latest")

    model_llm = start_prompt | llm 

    return model_llm

# init Model MiniLM
@st.cache_data
def init_model_MiniLM():
    # pre-trained model
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# Based on an input anime descrption, search recommended animes from LLM
def search_recommended_animes_from_llm(input_anime_description, filter_hentai_on):
    input_clean = re.sub("[^A-Za-z]+", " ", str(input_anime_description)).lower()

    # Prompt string 
    sys_prompt="""
    You are a positive and negative element extractor.

    Analyze the user's sentence and extract:
    - what the user wants (positive),
    - what the user explicitly wants to avoid (negative).

    If the user mentions a well-known title (such as an anime, movie, game, etc.) in what they want to avoid, extract it separately.

    Return your response as a JSON object with three fields:
    - positive: a single string summarizing with key-words what the user wants.
    - negative: a single string summarizing with key-words what the user wants to avoid.
    - title: the name of the title the user wants to avoid, if any (e.g., an anime, show, movie); return `null` if none is found.

    {{format_instructions}}
    """

    model_llm = init_model_llm(sys_prompt)
    parser = PydanticOutputParser(pydantic_object=OutputSchema_describe)

    # Get the response 
    response = model_llm.invoke({"text": input_clean, "format_instructions": parser.get_format_instructions()})
    input_positive_clean = parser.parse(response.content).positive
    input_negative_clean = parser.parse(response.content).negative
    input_title_clean = parser.parse(response.content).title

    # User wants ...
    if input_positive_clean:
        model = init_model_MiniLM()
        df_emb = load_synopsis_embedding()
        df_animes = load_animes()
        # Add genres
        df_emb_with_genre = df_emb.merge(df_animes[["uid", "genre"]], on="uid", how="inner")

        # Hentai filter
        if filter_hentai_on:
            col_category = "genre"
            category = "Hentai"
        else:
            col_category = None
            category = None

        result_df_negative = pd.DataFrame(columns=["uid", "similarity"])

        # Find all animes that are the closest to the user's preferences
        input_positive_embedding = model.encode(input_positive_clean)
        result_df_positive = pd.DataFrame(closest_similarity(input_positive_embedding, df_emb_with_genre, col_category, category), columns=['uid','similarity']).head(20)


         # User don't want ...
        if input_negative_clean:

            # Find all animes that are the closest to what the user wants to avoid
            input_negative_embedding = model.encode(input_negative_clean)
            result_df_negative = pd.DataFrame(closest_similarity(input_negative_embedding, df_emb_with_genre, col_category, category), columns=['uid','similarity']).head(20) 
           
        # User don't want a Title ...
        if input_title_clean:
            mask = df_animes["title"].str.lower().apply(lambda title: any(mot in title for mot in input_negative_clean.lower().split()))
            result_df_title_negative = df_animes[mask]
            result_df_negative = pd.concat([result_df_negative, result_df_title_negative], ignore_index=True)   

        # We exclude the anime the user doesn't want from those they do want
        result_df_final = result_df_positive[~result_df_positive['uid'].isin(result_df_negative['uid'])]
        result_df_final = result_df_final.sort_values(by='similarity', ascending=False)

        return result_df_final.head()
    
    else:
         raise ValueError("Sorry, your input doesn't allow us to generate any recommendations. Please try rephrasing your request with more details or clarity.")
    

## RECO_06 : diffusion list for new content

@st.cache_data
def explode_favorite_anime_profile(df):
    df["favorites_anime"] = df["favorites_anime"].apply(ast.literal_eval)
    df_favorites = df[["profile", "favorites_anime"]].copy().explode("favorites_anime")
    df_favorites = df_favorites.dropna(subset=["favorites_anime"])
    df_favorites["favorites_anime"] = df_favorites["favorites_anime"].astype("int64")

    return df_favorites


def generate_diffusion_list(target):
    
    model = init_model_MiniLM()
    df_emb = load_synopsis_embedding()
    df_profiles = load_profiles()
    df_favorites = explode_favorite_anime_profile(df_profiles)

    target = re.sub("[^A-Za-z]+", " ", str(target)).lower()
    target = model.encode(target)

    similarity_df = closest_similarity(target, df_emb)

    # filter by similarity
    closest = similarity_df[similarity_df['similarity'] >= 0.5].sort_values(by='similarity', ascending=False)

    df_merged = df_favorites.merge(closest, left_on='favorites_anime', right_on='uid', how='inner')
    grouped_df = df_merged.groupby('profile').agg({'uid': list}).reset_index()

    # sorted by uid lenght
    sorted_profile = grouped_df.sort_values(by="uid", key=lambda x: x.str.len(), ascending=False)

    return sorted_profile

# STREAM_02
@st.dialog("Anime overview")
def display_synopsis(anime):             
    if anime is not None:
        write_col("Title : " + anime["title"])
        write_col(anime["synopsis"])
        write_col_with_label(anime["episodes"], "Episodes : ")
##

def extract_animes_from_uid(df_animes, df_uid):
    
    uids = {uid for sub in df_uid['uid'] for uid in sub}
    selected_animes = df_animes[df_animes['uid'].isin(uids)][['title','uid']].reset_index(drop=True)
       
    return selected_animes


# RECO_04

# init Model LLM
@st.cache_resource
def init_model_llm_reviews():
# Prompt string 
    sys_prompt_reviews="""
    You are a specialized in analysing the positive and negative elements in reviews of animes left by different users. Your task is to provide user with a summary of reviews left by other users on the platform to help them determine whether to watch that anime or not.

    Ignore the "more pics" citation at the beginning of each review, as it refers to something outside of it.

    Analyze the users' sentence and extract, if they are encountered:
    - the positive points expressed in the reviews,
    - the negative points on which the criticism is based.

    Your response shall summarize the key aspects of the anime, taking into account that there are several reviews left by as many users, but without explicitly mentioning the amount of reviews left. Please be relatively measured with the way you present negative criticism.
    You shall also take into account the proportion difference between positive and negative feedbacks.

    Return your response as a JSON object containing up to two fields:
    If no positive feedback is provided, ignore the generation of the sentence, and proceed to the next point.
    - positive: a single string summarizing the positive aspects raised, starting with "Users liked:"
    If no negative aspect is mentioned, or if they are disproportionately rare compared to the positive feedback, ignore the generation of the sentence. Otherwise, proceed as follows :
    - negative: a single string summarizing the negative aspects raised, starting with "Users disliked:".

    {{format_instructions}}
    """

    # Define system prompt
    start_prompt_reviews = ChatPromptTemplate.from_messages([
        ("system", sys_prompt_reviews),
        ("user", "{text}")
        ])

    # Don't forget your API Key : export MISTRAL_API_KEY=...

    # Let's instanciate a model 
    llm_reviews = ChatMistralAI(model="mistral-medium-latest")

    model_llm_reviews = start_prompt_reviews | llm_reviews 

    return model_llm_reviews

def generate_review_summary(given_anime_uid):    
    sys_prompt_reviews ="""
    You are a specialized in analysing the positive and negative elements in reviews of animes left by different users. Your task is to provide user with a summary of reviews left by other users on the platform to help them determine whether to watch that anime or not.

    Ignore the "more pics" citation at the beginning of each review, as it refers to something outside of it.

    Analyze the users' sentence and extract, if they are encountered:
    - the positive points expressed in the reviews,
    - the negative points on which the criticism is based.

    Your response shall summarize the key aspects of the anime, taking into account that there are several reviews left by as many users, but without explicitly mentioning the amount of reviews left. Please be relatively measured with the way you present negative criticism.
    You shall also take into account the proportion difference between positive and negative feedbacks.

    Return your response as a JSON object containing up to two fields:
    If no positive feedback is provided, ignore the generation of the sentence, and proceed to the next point.
    - positive: a single string summarizing the positive aspects raised, starting with "Users liked:"
    If no negative aspect is mentioned, or if they are disproportionately rare compared to the positive feedback, ignore the generation of the sentence. Otherwise, proceed as follows :
    - negative: a single string summarizing the negative aspects raised, starting with "Users disliked:".

    {{format_instructions}}
    """    
    model_llm_reviews = init_model_llm(sys_prompt_reviews)
    parser = PydanticOutputParser(pydantic_object=OutputSchema_review)
    
    df_reviews=load_reviews()
    input=df_reviews[df_reviews['anime_uid']==given_anime_uid]['text'].apply(clean_text)
    if len(input) == 0:
        output = ["This anime has no review yet! You can watch it and review it yourself!"]
    else:        
        response = model_llm_reviews.invoke({"text": input, "format_instructions": parser.get_format_instructions()})
        output_positive = parser.parse(response.content).positive
        output_negative = parser.parse(response.content).negative
        ai_notice = f'Response generated by Mistral AI, based on {len(input)} reviews'
        output = [output_positive, output_negative, ai_notice]
    return output

#Display AI review summary
@st.dialog("Review summary : powered by Mistral AI")
def display_review(given_anime_uid):             
    if given_anime_uid is not None:
        response = generate_review_summary(given_anime_uid)
        for text in response:
            st.markdown(text)

