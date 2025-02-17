import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os
if not os.path.exists('similarity.pkl'):
    st.info("Downloading large file from Google Drive...")
    gdown.download("https://drive.google.com/file/d/1zJNHVt53PzbZUCuMXVGrYgAs8AgDAX23/view?usp=sharing", 'similarity.pkl', quiet=False)

def fetch_poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=78aa1355b336e90fc0fdb850393823a0'.format(movie_id))
    data=response.json()
    return 'https://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distance=similarity[movie_index]
    movie_list=sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies=[]
    recommended_movies_poster=[]
    for i in movie_list:
        movie_id=movies.iloc[i[0]].id
        #Fetch Poster from api
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

st.title('Movie Recommendation System')
movies_dict= pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)
similarity=pickle.load(open('similarity.pkl','rb'))
values=movies["title"].values
# SELECT BOX
selected_movie_name=st.selectbox(
    'How would ',
    values
)
if st.button('Show Similar'):
    names,posters = recommend(selected_movie_name)
    cols=st.columns(5)
    for col, name, poster in zip(cols, names, posters):
        with col:
            st.text(name)
            st.image(poster)

