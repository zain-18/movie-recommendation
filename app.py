import  pickle as pk
import  pandas as pd
import streamlit as st
import requests
st.title('Movie Recommender System')

movies_list=pk.load(open('movies_list.pkl','rb'))
similarity=pk.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_list)

# fetch poster from api
def fetch_poster(movie_id):
    url='https://api.themoviedb.org/3/movie/{}?api_key=7a837c73f9b2ce6907272363c465910d&language=en-US'.format(movie_id)
    data = requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    full_path="https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies_name=[]
    recommended_movies_posters=[]
    for i in movie_list:
        recommended_movies_name.append(movies['title'][i[0]])
        #calling fetch_poster method
        recommended_movies_posters.append(fetch_poster(movies['id'][i[0]]))
    return recommended_movies_name,recommended_movies_posters

selected_movie_name = st.selectbox(
     'Select the movie Name',
     movies['title'])

if st.button('Recommend'):
    recommended_movies_name,recommended_movies_posters=recommend(selected_movie_name)
    col1, col2, col3,col4,col5 = st.columns(5)

    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_posters[0])

    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_posters[2])

    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_posters[3])

    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_posters[4])






