import streamlit as st
import pandas as pd
import pickle
import requests
import time
from navigation import make_sidebar

st.set_page_config(layout="wide")

make_sidebar()

st.title("Movie Recommendation System")

apiKey = "23e8d4aac45b466a04e37b74f573a2bf"

mapping = pd.read_csv('dataset/links_small.csv')

movies = pickle.load(open('saved_models/movie_info.pkl', 'rb'))
movies_list = movies['title'].values

ratings = pickle.load(open('saved_models/ratings_info.pkl', 'rb'))
svd = pickle.load(open('saved_models/svd_model.pkl', 'rb'))
popular = pickle.load(open('saved_models/top_movies.pkl', 'rb'))

users_list = ratings.userId.unique()


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apiKey}&language=en-US"
    # st.text(url)
    time.sleep(0.01)
    data = requests.request('GET', url)
    data = data.json()
    full_path = 'https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/01/dark-knight-rises-fails.jpg'
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

if 'username' not in st.session_state:
    selected_user = 20
else:
    selected_user = st.session_state.username

def recommend_svd(movie):
    recommended_svd_posters = []
    userId = selected_user
    print(userId)
    total = ratings.movieId.unique()
    test = ratings[ratings.userId == userId]['movieId'].unique()
    print(test)
    remaining = list(set(total) - set(test))
    df = pd.DataFrame(remaining, columns=['movieId'])
    df['userId'] = userId
    df['est'] = df.apply(lambda row: svd.predict(row['userId'], row['movieId']).est, axis=1)
    print("DF: ", df)
    quantile = df.sort_values(by='est', ascending=False)['est'].quantile(0.75)
    filtered_movies = df[df.est > quantile]
    filtered_movies = pd.merge(filtered_movies, mapping, on='movieId')
    filtered_movies = filtered_movies.head(9)
    # Need to check for Hybrid
    # index = movies[movies['title'] == movie].index[0]
    # distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    # similarity_df = pd.DataFrame(distances[1:], columns=['tmdbId', 'similarity'])
    # final_ratings = pd.merge(filtered_movies, similarity_df, on='tmdbId').sort_values(by=['similarity', 'est'],
    #                                                                                   ascending=False)
    # final_ratings['weighted'] = final_ratings['est'] * 2 + final_ratings['similarity'] * 30
    # print(final_ratings)
    # final_ratings = final_ratings.sort_values('weighted', ascending=False).head(8)
    # print(final_ratings)
    movieIds = filtered_movies['tmdbId']
    print("Movies ID: ", movieIds)
    for tmdbId in movieIds[1:]:
        recommended_svd_posters.append(fetch_poster(tmdbId))
    return recommended_svd_posters


st.header('Top Trending in India')
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
with col1:
    # st.text(recommended_movie_names[0])
    st.image(fetch_poster(popular.iloc[0].id))
with col2:
    # st.text(recommended_movie_names[1])
    st.image(fetch_poster(popular.iloc[1].id))
with col3:
    # st.text(recommended_movie_names[2])
    st.image(fetch_poster(popular.iloc[2].id))
with col4:
    # st.text(recommended_movie_names[3])
    st.image(fetch_poster(popular.iloc[3].id))
with col5:
    # st.text(recommended_movie_names[4])
    st.image(fetch_poster(popular.iloc[4].id))
with col6:
    # st.text(recommended_movie_names[4])
    st.image(fetch_poster(popular.iloc[5].id))
with col7:
    # st.text(recommended_movie_names[4])
    st.image(fetch_poster(popular.iloc[6].id))
with col8:
    # st.text(recommended_movie_names[4])
    st.image(fetch_poster(popular.iloc[7].id))
#
selected_movie = st.selectbox("What would you like to watch?", movies_list)
#
# # st.image('https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/01/dark-knight-rises-fails.jpg')
#
if st.button('Show Similar Movies'):
    st.header('What other viewers liked')
    recommended_svd_movie_posters = recommend_svd(selected_movie)
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        # st.text(recommended_movie_names[0])
        st.image(recommended_svd_movie_posters[0])
    with col2:
        # st.text(recommended_movie_names[1])
        st.image(recommended_svd_movie_posters[1])
    with col3:
        # st.text(recommended_movie_names[2])
        st.image(recommended_svd_movie_posters[2])
    with col4:
        # st.text(recommended_movie_names[3])
        st.image(recommended_svd_movie_posters[3])
    with col5:
        # st.text(recommended_movie_names[4])
        st.image(recommended_svd_movie_posters[4])
    with col6:
        # st.text(recommended_movie_names[4])
        st.image(recommended_svd_movie_posters[5])
    with col7:
        # st.text(recommended_movie_names[4])
        st.image(recommended_svd_movie_posters[6])
    with col8:
        # st.text(recommended_movie_names[4])
        st.image(recommended_svd_movie_posters[7])
