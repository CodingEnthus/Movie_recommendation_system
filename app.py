import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie posters from TMDb API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)

    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"

    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"

# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Fetch actual movie_id, not index
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


st.markdown("""
    <style>
        /* Dark Theme */
        body {
            background-color: black;
            color: white;
            font-family: 'Arial', sans-serif;
        }

        /* Centered Header */
        .main-title {
            text-align: center;
            color: #ff6600;
            font-size: 40px;
            font-weight: bold;
        }

        /* Movie Title Style */
        .movie-title {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            color: #ffcc00;
            margin-top: 10px;
        }

        /* Movie Poster Styling */
        .movie-poster {
            display: block;
            margin: 0 auto;
            border-radius: 10px;
            box-shadow: 5px 5px 15px rgba(255, 255, 255, 0.2);
        }

        /* Recommend Button Style */
        .stButton>button {
            background-color: #ff6600 !important;
            color: white !important;
            font-size: 18px !important;
            border-radius: 10px !important;
            padding: 10px 20px !important;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 class='main-title'>🎬 Movie Recommender System 🎥</h1>", unsafe_allow_html=True)

# Movie Selection
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

# Recommend Button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)  # Create 5 columns for recommendations
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.markdown(f'<p class="movie-title">{name}</p>', unsafe_allow_html=True)
            st.markdown(f'<img class="movie-poster" src="{poster}" width="150">', unsafe_allow_html=True)
