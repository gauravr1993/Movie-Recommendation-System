from navigation import make_sidebar
import streamlit as st
import pandas as pd
import pickle
import requests
import time

st.set_page_config(layout="wide")

make_sidebar()
st.title("Movie Recommendation System")

apiKey = "23e8d4aac45b466a04e37b74f573a2bf"
movies = pickle.load(open('saved_models/movie_info.pkl', 'rb'))
movies_list = movies['title'].values
movies_df = pickle.load(open('saved_models/movie_genre_info.pkl', 'rb'))

genres_list = ['Animation','Comedy','Family','Adventure','Fantasy','Romance','Drama','Action','Crime','Thriller','Horror','History','ScienceFiction','Mystery','War','Foreign','Music','Documentary','Western']

selected_genres = st.multiselect("Choose 2-4 genres to get started?", genres_list)

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


def get_similar_genre_movies(user_genres):
    recommended_movies, recommended_posters = [], []
    movies_df['calculated'] = 0
    for genre in user_genres:
        movies_df['calculated'] += movies_df[genre]
    movies_info = (movies_df.sort_values(by='calculated', ascending=False).head(10))
    print(movies_info.calculated)
    movies_df.drop('calculated', axis=1, inplace=True)
    for _, row in movies_info.iterrows():
        movie_id = row.id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movies.append(row.title)
    return recommended_movies, recommended_posters


if st.button('Show Recommendation'):
    st.subheader("Here are top picks for you")
    recommended_movie_names, recommended_movie_posters = get_similar_genre_movies(selected_genres)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        # st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        # st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        # st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
    with col6:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[5])
    with col7:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[6])
    with col8:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[7])