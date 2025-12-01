import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=ea73bd4d1279efce734d85af5a776cec"
    print("Fetching:", url)

    response = requests.get(url)

    print("Status Code:", response.status_code)
    print("JSON:", response.text)

    data = response.json()

    if "poster_path" not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    recommend_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies, recommend_movies_poster

movies_dist = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dist)
st.title("Movie Recommender System")
Selected_movie_name = st.selectbox('How would you like to recommend movies?',movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(Selected_movie_name)
    col1, col2, col3 ,col4 ,col5 = st.columns(5)
    with col1:
        st.write(names[0])
        st.image(posters[0])
    with col2:
        st.write(names[1])
        st.image(posters[1])
    with col3:
        st.write(names[2])
        st.image(posters[2])
    with col4:
        st.write(names[3])
        st.image(posters[3])
    with col5:
        st.write(names[4])
        st.image(posters[4])
