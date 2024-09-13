from navigation import make_sidebar
import streamlit as st
import pandas as pd
import pickle
import requests
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide")

make_sidebar()

model = SentenceTransformer('all-MiniLM-L6-v2')
st.title("Movie Recommendation System")
apiKey = "23e8d4aac45b466a04e37b74f573a2bf"
mapping = pd.read_csv('dataset/links_small.csv')
movies = pickle.load(open('saved_models/movie_info.pkl', 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('saved_models/similarity_matrix.pkl', 'rb'))
popular = pickle.load(open('saved_models/top_movies.pkl', 'rb'))
sentence_embeddings = pickle.load(open('saved_models/sentence_embeddings.pkl', 'rb'))

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={apiKey}&language=en-US"
    time.sleep(0.01)
    data = requests.request('GET', url)
    data = data.json()
    full_path = 'https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/01/dark-knight-rises-fails.jpg'
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    recommended_movies = []
    recommended_posters = []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:9]:
        movie_id = movies.iloc[i[0]].id
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_posters
#
#
def get_sentence_embedding_movie(movie):
    print(movie)
    overview = movies[movies['title'] == movie]['overview'].values[0]
    print(overview)
    user_input_embedding = model.encode([overview])
    similarities = cosine_similarity(user_input_embedding, sentence_embeddings)
    similar_movies = sorted(list(enumerate(similarities[0])), reverse=True, key=lambda x: x[1])
    recommended_movies, recommended_posters = [], []
    for i, el in similar_movies[1:9]:
        movie_id = movies.iloc[i].id
        print(movies.iloc[i].title)
        recommended_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i].title)
    return recommended_movies, recommended_posters

selected_movie = st.selectbox("What would you like to watch?", movies_list)
# #
# # # st.image('https://static1.colliderimages.com/wordpress/wp-content/uploads/2022/01/dark-knight-rises-fails.jpg')
# #
if st.button('Show Similar Movies'):
    st.subheader('Based on this (Sentence Transformers)')
    recommended_movie_names, recommended_movie_posters = get_sentence_embedding_movie(selected_movie)
    recommended_movie_names_cv, recommended_movie_posters_cv = recommend(selected_movie)
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
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

    st.subheader('Based on this (Count Vectorizer)')

    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        # st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters_cv[0])
    with col2:
        # st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters_cv[1])
    with col3:
        # st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters_cv[2])
    with col4:
        # st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters_cv[3])
    with col5:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters_cv[4])
    with col6:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters_cv[5])
    with col7:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters_cv[6])
    with col8:
        # st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters_cv[7])