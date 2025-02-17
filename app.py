import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Fix Google Drive download link (Extract File ID)
similarity_file_id = "1zJNHVt53PzbZUCuMXVGrYgAs8AgDAX23"  # Extracted from your link
similarity_file_path = "similarity.pkl"

# Download if file is missing
if not os.path.exists(similarity_file_path):
    st.info("Downloading large file from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={similarity_file_id}", similarity_file_path, quiet=False)


# Function to fetch movie poster
def fetch_poster(movie_id):
    api_key = "78aa1355b336e90fc0fdb850393823a0"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500/' + data.get('poster_path', '')  # Handle missing poster case
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


# Recommendation function
def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distance = similarity[movie_index]
        movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []
        for i in movie_list:
            movie_id = movies.iloc[i[0]].id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_poster
    except IndexError:
        return [], []


# Streamlit UI
st.title('🎬 Movie Recommendation System')

# Load movie data
try:
    movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open(similarity_file_path, "rb"))
    values = movies["title"].values
except FileNotFoundError:
    st.error("Error: Required files are missing. Make sure 'movie_dict.pkl' and 'similarity.pkl' exist.")
    st.stop()

# Movie selection dropdown
selected_movie_name = st.selectbox("Select a Movie 🎥", values)

# Show recommendations
if st.button('Show Similar'):
    names, posters = recommend(selected_movie_name)

    if names:
        cols = st.columns(len(names))  # Dynamically adjust columns
        for col, name, poster in zip(cols, names, posters):
            with col:
                st.text(name)
                st.image(poster)
    else:
        st.warning("No similar movies found!")
