from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import requests

app = FastAPI(title="Movie Recommender API")

# Allow all origins (you can restrict to your frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data
movies_dist = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dist)

TMDB_API_KEY = "ea73bd4d1279efce734d85af5a776cec"

def fetch_poster(movie_id: int):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()
    if "poster_path" not in data or data['poster_path'] is None:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def recommend(movie: str):
    if movie not in movies['title'].values:
        return [], []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

# Root route
@app.get("/")
def read_root():
    return {"message": "Movie Recommender API is live!"}

# Recommendation endpoint
@app.get("/recommend/")
def get_recommendations(movie: str):
    names, posters = recommend(movie)
    return {"recommended_movies": names, "posters": posters}
