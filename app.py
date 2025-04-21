import os
import pickle
import streamlit as st
import requests

st.header("Movies Recommendation System Using Machine Learning")

# Handle potential file path issues
try:
    movies = pickle.load(open('C:\Python Project\Movie Recomender\Artificats\movie_list.pkl', 'rb'))  # Assuming Windows path
    similarity = pickle.load(open('C:\Python Project\Movie Recomender\Artificats\similaryty_list.pkl', 'rb'))
except FileNotFoundError:
    st.error("Error loading data files. Please ensure correct file paths.")
    exit()  # Terminate if data files cannot be loaded

movie_list = movies['title'].values

selected_movie = st.selectbox('Type or select a movie to get recommendation', movie_list)

def fetch_poster(movie_id, retries=3):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=49f0161dcfc2c2e23dc394325754801e".format(movie_id)
    for attempt in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    full_path = "http://image.tmdb.org/t/p/w500/" + poster_path
                    return full_path
                else:
                    #st.warning("Poster unavailable for this movie.")
                    return None
            else:
                #st.error(f"Error fetching poster: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < retries - 1:
               # st.warning(f"Error fetching poster. Retrying attempt {attempt+1}...")
                continue
            else:
                #st.error(f"Failed to fetch poster after {retries} attempts: {e}")
                return None  # Indicate persistent error
    return None  # Should not be reached if retries are successful

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies_name = []
    recommended_movies_poster = []
    for i in distances[1:11]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)

    return recommended_movies_name, recommended_movies_poster

if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)

    # Handle potential issues with missing posters
    if None in recommended_movies_poster:
        st.warning("Some recommended movie posters might be unavailable.")

    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        if recommended_movies_name[i] and recommended_movies_poster[i]:  # Check for both name and poster
            with col1 if i == 0 else col2 if i == 1 else col3 if i == 2 else col4 if i == 3 else col5:
                st.text(recommended_movies_name[i])
                st.image(recommended_movies_poster[i])