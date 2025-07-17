import streamlit as st
import pandas as pd
import plotly.express as px
import ast

from utils.common import load_animes, load_profiles, load_reviews

#load data
df_animes = load_animes()
df_profiles = load_profiles()
df_reviews = load_reviews()

st.markdown("# 📈 EDA")

st.markdown("""
Welcome to the EDA section!

Here, we will seek to analyze the data gathered through scraping on the platform dedicated to japanese animation MyAnimeList (myanimelist.net)
This data has been collected in january of 2020, and includes tables for :
- anime (more than 16k entries)
- user profiles (more than 47k entries)
- reviews (more than 130k entries)
            
The dataset we are using is available on Kaggle : https://www.kaggle.com/datasets/marlesson/myanimelist-dataset-animes-profiles-reviews

Here, we explore the anime dataset to better understand its structure, trends, and key insights.  
You will find visualizations and statistics about:

- Most common anime genres
- The top 10 best rated animes, and their average scores
- The 10 most reviewed animes
- The age and gender repartition of the user base for the platform
- The amount of reviews by anime (data for the top 10 best rated entries)
- The amount of reviews for the 10 most viewed entries

These insights help guide the recommendation system and ensure data quality.
""")

st.subheader("1) Anime-based analysis")

st.markdown("First, let's get the most represented genres")

df_animes['genre'] = df_animes['genre'].apply(ast.literal_eval)
df_exploded = df_animes.explode('genre')
genre_count = pd.DataFrame(df_exploded['genre'].value_counts().reset_index(name='count').head(10))

count = px.bar(genre_count,
               x='genre',
               y='count', 
               labels={'genre': 'Genre', 'count': 'Count'},
               text='count',
               title="10 most represented genres",
               template="plotly_dark", 
               color_discrete_sequence=px.colors.qualitative.Dark2)

st.plotly_chart(count, use_container_width=True)

st.markdown("Let's find out the average score of the 10 best ranked animes")

rank = df_animes.sort_values(by='ranked').head(10)

top_rank = px.bar(rank,
                        x='title',
                        y='score',
                        labels={'title': 'Title', 'score': 'Score'},
                        text='ranked',
                        title='Top ranked animes and their average score',
                        template="plotly_dark", 
                        color_discrete_sequence=px.colors.qualitative.Pastel)
top_rank.update_yaxes(range=[8.9,9.4])

st.plotly_chart(top_rank, use_container_width=True)

st.markdown("Let's now find out the most popular animes based on their viewership")

pop = df_animes.sort_values(by='popularity')
pop.head(10)
pop10 = pop.head(10)

top_pop = px.bar(pop10,
                        x='title',
                        y='members',
                        labels={'title': '', 'members': 'Popularity'},
                        text='members',
                        title='Most popular animes and their viewership',
                        template="plotly_dark", 
                        color_discrete_sequence=px.colors.qualitative.Vivid)
top_pop.update_yaxes(range=[1000000,2000000])

st.plotly_chart(top_pop, use_container_width=True)

st.markdown("""Observations :
It appears the most popular animes by viewership differ from the best ranked ones, those can be more flawed but also more appealing to the general public,
whilst the best ranked ones, for some, can be considered more niche.
            
In spite of the database only containing about 46k registered users, we can see the viewership amounts to millions of viewers. This is due to the fact the website allows for the creations of "viewing lists" of animes even for non registered users. Data is then kept in cache on their browser and they then have to return to the site through the same computer and browser in order to access their list. This explains why there are millions of viewers registered on the top entries.
""")

st.subheader("2) User-based analysis")


age_graph = px.histogram(df_profiles,
                         x='age',
                         color='gender',
                         labels={'count': 'Count', 'age': 'Age'},
                         title='Age and gender distribution that users declared for themselves (sample of 22k)',
                         color_discrete_sequence=px.colors.qualitative.Alphabet_r,
                         template='plotly_dark')

st.plotly_chart(age_graph, use_container_width=True)

st.markdown("""The median age of the user base is 25 years old. The mean age is around 26 years old.
Out of around 30k users whose age can be calculated and who filled a gender information, more than 2 thirds are men, 1 third are women. A small proportion (less than 500 people) declare as non binary.
            
Observations :
It appears some users have voluntarily declared an age that is unrepresentative of their real age (some users are aged 0, some older than 90).
According to the Wikipedia article on MyAnimeList, the website exists since 2004. Which means that users simply entering the current day's date as their birthday when joining can be up to 15 years old by the point the data has been collected.
So we have to be aware of the potential inaccuracy of the data around its edges.

However, given the population watching anime tends to be fairly young, it is safe to assume that the median and mean of the age remain representative of the reality, especially given the fact we have skimmed through many date formats to only keep the users who filled a complete and valid date (for example, we did not take into account the many users who only filled a day and a month as their birthday. Only date formats containing a year in the form of 4 consecutive numbers were considered).
""")
            
st.subheader("3) Review-based analysis")


top10_anime_uid = rank['uid'].tolist()
reviews_for_top10 = df_reviews[df_reviews['anime_uid'].isin(top10_anime_uid)]
reviews_for_top10 = pd.merge(reviews_for_top10, df_animes, left_on='anime_uid', right_on='uid')

reviews_for_top10 = reviews_for_top10[reviews_for_top10['ranked'] <= 10]

columns_to_keep = ['uid_x', 'profile',	'anime_uid', 'text','score_x', 'scores', 'link_x', 'title', 'ranked', 'score_y', 'popularity', 'members']
reviews_for_top10 = reviews_for_top10[columns_to_keep]

df_revtop = reviews_for_top10['title'].value_counts().reset_index()
df_revtop.columns = ['title', 'count']

reviews_top = df_revtop.merge(reviews_for_top10[['title', 'ranked']], on='title', how='left').drop_duplicates()
reviews_top = reviews_top.sort_values(by='count', ascending=False)

reviews_top10 = px.bar(reviews_top,
                        x='title',
                        y='count',
                       labels={'count': 'Amount of reviews', 'title': ''},
                        title='Amount of reviews on the top 10 best ranked animes (excluding top 3 entry for which data is missing)',
                        text='ranked',
                        height= 600,
                        color_discrete_sequence=px.colors.qualitative.Dark24_r,
                        template='plotly_dark'
                       )
reviews_top10.update_traces(textangle=0, textposition="outside")                      
st.plotly_chart(reviews_top10, use_container_width=True)



st.markdown("""
Observation : Bias in some of the models due to missing data in reviews.
            
Here, we see that among the top 10 best rated entries, one is missing. the 3rd ranked entry, Hunter X Hunter (2011), does not appear on the graph due to its reviews' data not being collected through the scraping process that permitted the dataset's construction.

This means that models relying on reviews for recommendations will exclude the animes that saw their reviews not being collected, which includes some recommendation-worthy titles such as HxH. 

Beside, we have to take into account the release date of the titles. For example, the most recent entry in this top 10 is top 5 "Shingeki no Kyojin Season 3 Part 2" ("Attack on Titan"), which finished airing july 2019, less than 6 months before the collection of the data (january the 5th 2020). This means that some entries have had less time to accumulate reviews, and this can possibly weight in the recommendation models based on them.           
""")


mostpop_anime_uid = pop10['uid'].tolist()
reviews_for_mostpop = df_reviews[df_reviews['anime_uid'].isin(mostpop_anime_uid)]
reviews_for_mostpop = pd.merge(reviews_for_mostpop, df_animes, left_on='anime_uid', right_on='uid')

reviews_for_mostpop = reviews_for_mostpop[reviews_for_mostpop['popularity'] <= 10]
reviews_for_mostpop = reviews_for_mostpop[columns_to_keep]

df_mostpop = reviews_for_mostpop['title'].value_counts().reset_index()
df_mostpop.columns = ['title', 'count']

reviews_pop = df_mostpop.merge(reviews_for_mostpop[['title', 'popularity']], on='title', how='left').drop_duplicates()
reviews_pop = reviews_pop.sort_values(by='count', ascending=False)

reviews_mostpop = px.bar(reviews_pop,
                       x='title',
                       y='count',
                       labels={'count': 'Amount of reviews', 'title': ''},
                        title='Amount of reviews on the most popular entries',
                        text='popularity',
                        height= 600,
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        template='plotly_dark'
                       )
reviews_mostpop.update_traces(textangle=0, textposition="outside")
st.plotly_chart(reviews_mostpop, use_container_width=True)


st.markdown("""
Observation : Notable disproportion in the amount of reviews for the most popular entries. Some entries seem to generate more engagement, possibly with mixed reviews being more numerous (as is the case for most reveiwed entry "Sword Art Online").     
""")