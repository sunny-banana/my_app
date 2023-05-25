#core packages
import ast

import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
import pickle
import requests
from PIL import Image
import base64
from passlib.hash import bcrypt_sha256
import pymongo
import bcrypt
from passlib.hash import bcrypt
from pymongo import MongoClient

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017")

# Access the database
db = client["users"]

# Access collections
collection = db["users"]
# Define Streamlit session state
class SessionState:
    def __init__(self):
        self.logged_in = False

# Create a session state object
session_state = SessionState()
def get_movie_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))

     data = response.json()


     return "https://image.tmdb.org/t/p/w500" + data['poster_path']

def get_movie_overview(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
               movie_id))

     data = response.json()

     return data['overview']


def get_movie_rating(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
                    movie_id))

     data = response.json()

     return data['vote_average']

def get_movie_genre(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
               movie_id))

     data = response.json()

     return data['genres']

def get_movie_release_date(movie_id):
     response = requests.get(
           'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
                movie_id))

     data = response.json()

     return data['release_date']

def get_movie_runtime(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
                movie_id))

     data = response.json()

     return data['runtime']

def get_movie_status(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
               movie_id))

     data = response.json()

     return data['status']

def get_movie_link(movie_id):
     response = requests.get(
          'https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(
           movie_id))

     data = response.json()

     return data['homepage']


def recommend(movie):
     recommended_movies = []
     recommended_movies_posters =[]
     recommended_movies_overview = []
     recommended_movies_rating = []
     recommended_movies_genre = []
     recommended_movies_release_date = []
     recommended_movies_runtime = []
     recommended_movies_status = []
     recommended_movies_link = []

     movie_index = movies[movies['title'] == movie].index[0]

     distances = similarity[movie_index]

     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

     for i in movies_list:
          #error here was that it was using the index when it was originally movie_id = movies.i[0]
          movie_id = movies.iloc[i[0]].movie_id


          recommended_movies.append(movies.iloc[i[0]].title)
          # get movie poster from TMDB  API
          recommended_movies_posters.append(get_movie_poster(movie_id))
          recommended_movies_overview.append(get_movie_overview(movie_id))
          recommended_movies_rating.append(get_movie_rating(movie_id))
          recommended_movies_genre.append(get_movie_genre(movie_id))
          recommended_movies_release_date.append(get_movie_release_date(movie_id))
          recommended_movies_runtime.append(get_movie_runtime(movie_id))
          recommended_movies_status.append(get_movie_status(movie_id))
          recommended_movies_link.append(get_movie_link(movie_id))

     return recommended_movies, recommended_movies_posters, recommended_movies_overview,recommended_movies_rating, recommended_movies_genre, recommended_movies_release_date, recommended_movies_runtime, recommended_movies_status, recommended_movies_link

movies_dictionary = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dictionary)

similarity = pickle.load(open('similarity.pkl', 'rb'))

img = Image.open('icon.jpg')
#here we set a custom icon for the page
st.set_page_config(
                   page_icon=img,
                   layout='wide'
                   )


hide_menu_style = """
     <style>
     #MainMenu {visibility: hidden;}
     footer {visibility: hidden;}
     </style>
"""


@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
     with open(bin_file, 'rb') as f:
          data = f.read()
     return base64.b64encode(data).decode()


def set_png_as_page_bg(png_file):
     bin_str = get_base64_of_bin_file(png_file)
     page_bg_img = '''
    <style>
    .stApp {
  background-image: url("data:image/png;base64,%s");
  background-size: cover;
  background-repeat: no-repeat;
}
    </style>
    ''' % bin_str

     st.markdown(page_bg_img, unsafe_allow_html=True)
     return

hide_img_fs = '''
              <style>
              button[title="View fullscreen"]{
                  visibility: hidden;}
              </style>
              '''

st.markdown(hide_img_fs, unsafe_allow_html=True)



set_png_as_page_bg('movie_2.jpg')

# st.markdown(hide_menu_style, unsafe_allow_html=True)
#
st.title("S-MovieRec System")
#
menu = ["Home", "Login", "Sign Up" , "Recommend", "About", "Help"]

def home_page():
    st.subheader("Home Page")
    st.image("bg_image.jpg")

    st.write(
        "Welcome to the home of movies. Use the menu to your left to explore other pages and begin getting recommendations!")

def recommender_page():
    st.subheader('Recommender Page')

    movie_selected = st.selectbox(
        'Enter title of movie below',
        movies['title'].values)

    if st.button('Give Recommendation'):
        # names, posters = recommend(movie_selected)
        names, posters, overview, rating, genre, release_date, runtime, status, link = recommend(movie_selected)

        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

        with col1:
            st.markdown(names[0])
            st.image(posters[0])
            # st.text_area("Overview:", overview[0], height=200)
            st.write("Rating:", rating[0])
            # st.write("Genre", genre[0])
            st.write("Date:", release_date[0])
            st.write("Runtime:", runtime[0], "mins")
            # st.write("Status:", status[0])
            st.write("Homepage:", link[0])

        # with col2:
        #     container = st.container()
        #     container.markdown(names[1])
        #     container.image(posters[1])
        #     st.text_area("Overview:", overview[1], height=200)
        #     st.write("Rating:", rating[1])
        #     # st.write("Genre", genre[0])
        #     st.write("Date:", release_date[1])
        #     st.write("Runtime:", runtime[1], "mins")
        #     # st.write("Status:", status[1])
        #     st.write("Homepage:", link[1])
        #
        # with col3:
        #     container = st.container()
        #     container.markdown(names[2])
        #     container.image(posters[2])
        #     st.text_area("Overview:", overview[2], height=200)
        #     st.write("Rating:", rating[2])
        #     # st.write("Genre", genre[0])
        #     st.write("Date:", release_date[2])
        #     st.write("Runtime:", runtime[2], "mins")
        #     # st.write("Status:", status[2])
        #     st.write("Homepage:", link[2])
        #
        # with col4:
        #     container = st.container()
        #     container.markdown(names[3])
        #     container.image(posters[3])
        #     st.text_area("Overview:", overview[3], height=200)
        #     st.write("Rating:", rating[3])
        #     # st.write("Genre", genre[0])
        #     st.write("Date:", release_date[3])
        #     st.write("Runtime:", runtime[3], "mins")
        #     # st.write("Status:", status[3])
        #     st.write("Homepage:", link[3])
        #
        # with col5:
        #     container = st.container()
        #     container.markdown(names[4])
        #     container.image(posters[4])
        #     st.text_area("Overview:", overview[4], height=200)
        #     st.write("Rating:", rating[4])
        #     # st.write("Genre", genre[0])
        #     st.write("Date:", release_date[4])
        #     st.write("Runtime:", runtime[4], "mins")
        #     # st.write("Status:", status[4])
        #     st.write("Homepage:", link[4])

        # with 6:
        #
        #      st.markdown(names[5])
        #      st.image(posters[5])
        #      st.text_area("Overview:", overview[5], height=200)
        #      st.write("Rating:", rating[5])
        #      # st.write("Genre", genre[0])
        #      st.write("Date:", release_date[5])
        #      st.write("Runtime:", runtime[5], "mins")
        #      st.write("Status:", status[5])
def signup_page():
    st.title("Sign Up")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        user = collection.find_one({"username": username})
        if user:
            st.error("Username already exists. Please choose a different username.")
        else:
            # hashed_password = bcrypt.hash(password)
            user = {
                "username": username,
                "password": password
            }
            if password == confirm_password:

                user_data = {"username": username, "password": password}
                collection.insert_one(user_data)
                st.success("Account created successfully. You can now log in.")
                signup_successful = True
                if signup_successful:
                    if st.button("Login"):
                        st.experimental_rerun()
                        # Reload the app to navigate to the login page

            else:
                st.error("Passwords do not match.")


            collection.insert_one(user)



# Streamlit login page
def login_page():
    st.title("Log In")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Log In"):
        user = collection.find_one({"username": username, "password": password})
        if user and user["password"] == password:
            st.success("Login successful. Welcome, " + username + "!")
            st.write("Redirecting to the main page...")

            recommender_page()


            # st.experimental_rerun()  # Reload the app to navigate to the main page

    else:
            st.error("Invalid username or password")

def main():
    st.title("Streamlit App")

    def main():
        st.set_page_config(layout="wide")
        st.sidebar.title("Navigation")
        selection = st.sidebar.radio("Go to", ["Login", "Sign Up"])

        if selection == "Login":
            login_page()
        elif selection == "Sign Up":
            signup_page()

choice = st.sidebar.selectbox("Navigation", menu)



if choice == "Home":
    home_page()
elif choice == "Sign Up":
    signup_page()
elif choice == "Login":
    login_page()
elif choice == "Recommend":
    recommender_page()

elif choice == "About":
     st.subheader("About")

     txt = st.text_area('About us', '''
     S-MovieRec System is backed by a database of 5000 movies that span several decades and genres.
     
     
     It was built using data science techniques with the help of python libraries and the Streamlit framework
      
     
     Simply navigate to the "Recommend" page using the menu to the left and select any movie from the drop down menu to get recommendations. 
      
             ''', height=300)

elif choice == "Help":
     st.subheader("Help")
     st.text("You can reach us on: ")
     st.subheader("Email: s-movierec@helpdesk.com")
     st.subheader("Mobile: +2348097747445")

