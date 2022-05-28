import  pickle
import  pandas as pd
import streamlit as st
import requests
import gzip

pickle_movie = open("movies_list.pkl","rb")
movies_list=pickle.load(pickle_movie)

pickle_similarity = open("similarity.pkl","rb")
similarity=pickle.load(pickle_similarity)

st.title('Movie Recommender System')
#movies_list=pk.load(open('movies_list.pkl','rb'))
#similarity=pk.load(open('similarity.pkl','rb'))
movies=pd.DataFrame(movies_list)

# fetch  movie title,poster,genres
def fetch_poster(movie_id):
    url='https://api.themoviedb.org/3/movie/{}?api_key=7a837c73f9b2ce6907272363c465910d&language=en-US'.format(movie_id)
    data = requests.get(url)
    data=data.json()
    poster_path=data['poster_path']
    movie_title=data['original_title']
    genres=data['genres']
    genres_name=[]
    for i in range(len(genres)):
        genres_name.append(data['genres'][i]['name'])

    full_path="https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path,genres_name
# fetch actors & director name
def cast_crew(movie_id):
    url='https://api.themoviedb.org/3/movie/{}/credits?api_key=7a837c73f9b2ce6907272363c465910d&language=en-US'.format(movie_id)
    data=requests.get(url)
    data=data.json()
    cast=data['cast']
    crew=data['crew']
    actors_name=[]
    actors_poster=[]
    director_name=''
    producer_name=''
    for i in range(6):
        actors_name.append(cast[i]['name'])
        actors_poster.append("https://image.tmdb.org/t/p/w500/"+cast[i]['profile_path'])

    for i in range(len(crew)):
        if crew[i]['job']=='Director':
           director_name=crew[i]['name']

        if crew[i]['job']=='Producer':
            producer_name=crew[i]['name']

    return director_name,actors_name,actors_poster,producer_name
# fetch moive trailer key
def get_trailer(movie_id):
    url='https://api.themoviedb.org/3/movie/{}/videos?api_key=7a837c73f9b2ce6907272363c465910d&language=en-US'.format(movie_id)
    data=requests.get(url)
    data=data.json()
    video_id=data['results'][0]['key']
    return video_id
# Recommend movie
def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    movie_id = movies.loc[movies['title']==movie,'id'].iloc[0]
    distances=similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommended_movies_name=[]
    recommended_movies_posters=[]
    for i in movie_list:
        recommended_movies_name.append(movies['title'][i[0]])
        #calling fetch_poster method
        recommended_movies_posters.append(fetch_poster(movies['id'][i[0]])[0])
    return recommended_movies_name,recommended_movies_posters,movie_id

selected_movie_name = st.selectbox(
     'Select the movie Name',
     movies['title'])

#Button to get Movie values
if st.button('Recommend'):
    recommended_movies_name,recommended_movies_posters,movie_id=recommend(selected_movie_name)
    director_name, actors_name, actors_poster,producer_name = cast_crew(movie_id)
    movie_poster,genres_name=fetch_poster(movie_id)
    video_key=get_trailer(movie_id)

    st.subheader('Movie Trailer')
    with st.container():
        url='https://www.youtube.com/embed/{}'.format(video_key)
        st.video(url)


    #Expand container to see Movie Details

    with st.sidebar:
        with st.container():
         st.image(movie_poster,width=250)

        with st.container():
            st.header(selected_movie_name)
            st.subheader('Director: ' + director_name)
            st.subheader('Producer: ' + producer_name)
            st.subheader('Genres: ' + genres_name[0] + ',' + genres_name[1])




        st.title('Cast')

        with st.container():
            col1, col2, col3,col4,col5 = st.columns(5)

            with col1:
                st.caption(actors_name[0])
                st.image(actors_poster[0])

            with col2:
                st.caption(actors_name[1])
                st.image(actors_poster[1])

            with col3:
                st.caption(actors_name[2])
                st.image(actors_poster[2])

            with col4:
                st.caption(actors_name[3])
                st.image(actors_poster[3])

            with col5:
                st.caption(actors_name[4])
                st.image(actors_poster[4])


    # Columns to set Recommended Movies
    st.subheader('Recommended Movies')
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


#full_path,genres_name=fetch_poster(1995)






