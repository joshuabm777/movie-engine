"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st
import streamlit.components.v1 as components #html extensions
#st.set_page.config(layout='wide', initial_sidebar_state='expanded')
import streamlit_option_menu
from streamlit_option_menu import option_menu
import base64

import streamlit as st
from streamlit_option_menu import option_menu
import time
import requests

from streamlit_lottie import st_lottie
from streamlit_lottie import st_lottie_spinner


# Data handling dependencies
import pandas as pd
import numpy as np

#visualization tools
import matplotlib as plt
import seaborn as sns


# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')
ratings = pd.read_csv('resources/data/ratings.csv')
movies =pd.read_csv('resources/data/movies.csv')

# merge the two sets
#merged = ratings.merge(movies, on='movieId', how='inner')

# App declaration
def main():
    #st.sidebar.markdown('side')
    st.markdown(
        """
        <style>
        .reportview-container {
        background: url('resources/imgs/sample.jpg')
        }
        .sidebar .sidebar-content {
        background: url('resources/imgs/sample.jpg')
        }
        </style>
        """,
    unsafe_allow_html=True
)

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    with st.sidebar:
        st.write('Prime Movie Recommendation App')
        from PIL import Image
        image2= Image.open('resources/imgs/Brand2.png')
        st.image(image2, caption='SUREC ENGINES')
        
        
        
        page_selection = option_menu(
            menu_title = None, 
            options = ["Recommender System","Movie Facts","Exploratory Data Analysis","About",'Company'],
            icons = ['gear', 'film', 'camera2','envelope','building'],
            menu_icon='cast',
            default_index= 0,
            #orientation='horizontal',
            styles={"container":{'padding':'0!important', 'background_color': 'brown'},
                'icon': {'color': 'orange', 'font-size': '15px'},
                'nav-link': {
                    'font-size':'15px',
                    'text-align': 'left',
                    'margin': '0px',
                    '--hover-color': '#4BAAFF',
                },
                'nav-link-selected': {'background-color': '#6187D2'},
            }
        )
    #page_options = ["Recommender System","Movie Facts","Exploratory Data Analysis","About"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    #page_selection = st.sidebar.radio("Choose Option", page_options)        
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('First Choice',title_list[14930:15200])
        movie_2 = st.selectbox('Second Choice',title_list[25055:25255])
        movie_3 = st.selectbox('Third Choice',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except Exception as e:
                    st.write(e)
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i, j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")

    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection== "Movie Facts":
        #Header Contents
        st.write("# Movie Facts")
        images = ['resources/imgs/Movie_facts.jpg']
        for i in images:
            st.image(i,use_column_width=True)
        filters = ["Top rated Movies","High Budget Movies"]
        filter_selection = st.selectbox("Fact Check",filters)
        if filter_selection=="Top rated Movies":
            movie_list = pd.read_csv('resources/data/movies.csv')
            ratings = pd.read_csv('resources/data/ratings.csv')
            df = pd.merge(movie_list, ratings, on ='movieId',how='left')
            movie_ratings= pd.DataFrame(df.groupby('title')['rating'].mean())
            movie_ratings["Number_Of_Ratings"] = pd.DataFrame(df.groupby('title')['rating'].count())
            indes = movie_ratings.index
            new_list=[]
            for movie in indes:
                i = ' '.join(movie.split(' ')[-1])
                new_list.append(i)
            new_lists = []
            for i in new_list:
                if len(i)<2:
                    empty=i
                    new_lists.append(empty)
                elif i[0] == "(" and i[-1]==")" and len(i)==11:
                    R_strip = i.rstrip(i[-1])
                    L_strip = R_strip.lstrip(R_strip[0])
                    spaces = ''.join(L_strip.split())
                    data_type_int = int(spaces)
                    new_lists.append(data_type_int) 
                else:
                    new_lists.append(i)
            cnn = []
            for i in new_lists:
                if type(i)!=int:
                    i=0
                    cnn.append(i)
                else:
                    cnn.append(i)
            movie_ratings["Year"] = cnn
            def user_interaction(Year,n):
                list_movies=movie_ratings[movie_ratings['Year']==Year].sort_values('Number_Of_Ratings',ascending=False).index
                return list_movies[:n]
            selected_year = st.selectbox("Select Calender Year",range(1900,2020))
            no_of_outputs = st.radio("Total Number Of Movies",(5,10,20,50))
            output_list = user_interaction(selected_year,no_of_outputs)
            new_list = []
            for movie in output_list:
                updated_line = ' '.join(movie.split(' ')[:-1])
                updated_line = "+".join(updated_line.split())
                new_list.append(updated_line)
                #st.subheader(str(i+1)+'. '+j)
            url = "https://www.imdb.com/search/title/?title="
            movie_links = []
            for i in new_list:
                links = url+i
                movie_links.append(links)
            dict_from_list = dict(zip(output_list, movie_links))
            for items in dict_from_list:
                st.subheader(items)
                st.write("Read more[here](%s)" % dict_from_list[items])

    if page_selection == "Exploratory Data Analysis":
        
        st.title('Data Visualization Analysis')
        col1, col2 = st.columns(2)
        if st.checkbox("Ratings"):
            st.subheader("Movie Ratings and Average Ratings")
            with col1:
                st.image('resources/imgs/ratings.png',use_column_width=True, caption= 'It seems users have a neutral to positive overview of the movies in the dataset')

            with col2:    
                st.image('resources/imgs/average_ratings.png',use_column_width=True, caption= 'The mean rating around 3')

        # if st.checkbox("correlation"):
        #     st.subheader("Correlation between features")
        #     st.image('resources/imgs/correlation.png',use_column_width=ie)
        
        if st.checkbox("Actor wordcloud"):
            st.subheader("Top Actors")
            st.image('resources/imgs/popular_actors.png',use_column_width=True, caption='Popular names such as Morgan Freeman,Samuel Jackson-some of the biggest names in Hollywood, starring in blockbuster flicks regularly. A lorge portion of movies have no cast where a title cast should be')
        
        if st.checkbox("Genres"):
            st.subheader("Top Genres")
            st.image('resources/imgs/genre_frequency.png',use_column_width=True, caption='Drama is the most popular genre among the movies, showing up in over 25000 movies. Comedy and Thillers are next. About 5000 movies were not allocated a specific genre.')
                
        
        # if st.checkbox("movies released per year"):
        #     st.subheader("Movies released per year")
        #     st.image('resources/imgs/release_year.png',use_column_width=True)


        if st.checkbox("Directors"):
            st.subheader("Director with highest number of movies")
            st.image('resources/imgs/top_10_directors.png',use_column_width=True, caption = 'Woody Allen is the most occuring director, besides Luc Besson, and Stephen King.')
    if page_selection == "Company":
        st.subheader("ABOUT THE TEAM")
        col1, col2 = st.columns(2)
        with col1:
            from PIL import Image
            image1 = Image.open('resources/imgs/Brand4.png')
        
            st.image(image1, caption='SUREC ENGINES')

        with col2:
            st.write('Find Us:' )
            st.write('+254 704 118713')
            st.write('info@surecteam.com')
            st.write('www.surecengine.com')
            st.write('https://github.com/Keltings/Movie-Recommender-Engine')



        
        st.info("#### Who we are")
		# You can read a markdown file from supporting resources folder
        st.markdown("SUREC is technology company solving recommendation problems for ambitiuos businesses in Africa.\n Our mission is to build algorithms that would aid businesses in Africa to be more profitable, and can compete with businesses around the world.")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            from PIL import Image
            image2= Image.open('resources/imgs/Gathon.jpg')
            st.image(image2, caption='Milka Gathoni')

        with col2:
            from PIL import Image
            image2= Image.open('resources/imgs/mijan.jpeg')
            st.image(image2, caption='Samuel Mijan')

        with col3:
            from PIL import Image
            image2= Image.open('resources/imgs/Jessica.jpg')
            st.image(image2, caption='Jessica Njuguna')

        with col4:
            from PIL import Image
            image2= Image.open('resources/imgs/Sipho.jpg')
            st.image(image2, caption='Sipho Lukhele')

        with col5:
            from PIL import Image
            image2= Image.open('resources/imgs/kelida.jpg')
            st.image(image2, caption='Kelida Linda')
    if page_selection=='About':
            #markup(page_selection)
        st.write("### Oveview: Flex your Unsupervised Learning skills to generate movie recommendations")
        
        # You can read a markdown file from supporting resources folder
        if st.checkbox("Introduction"):
            st.subheader("Overview")
            st.write("""On the internet, where the number of choices is overwhelming, there is a need to filter, prioritize and efficiently deliver relevant information in order to reduce the problem of information overload, which has created a potential problem to many Internet users. Recommender systems solve this problem by searching through large volume of dynamically generated information to provide users with personalized content and services.""")
            st.write("""Recommender systems are information filtering systems that deal with the problem of information overload by filtering vital information fragment out of large amount of dynamically generated information according to user’s preferences, interest, or observed behaviour about item. Recommender system has the ability to predict whether a particular user would prefer an item or not based on the user’s profile.""")
            st.write("""Recommender systems are beneficial to both service providers and users. They reduce transaction costs of finding and selecting items in an online shopping environment. Recommendation systems have also proved to improve decision making process and quality.""")

        if st.checkbox("Task"):
            st.subheader("Unsupervised Learning Prediction")
            from PIL import Image
            image2= Image.open('resources/imgs/system.png')
            st.image(image2, caption='Build a Recommender System to recommend a movie')

            


        if st.checkbox("Data"):
            st.subheader("Data Overview")
            st.write("""The data consists of 10 million+ observations""")

            st.write("""For the Predictions, we will be using algorithm based on content or collaborative filtering, capable of accurately predicting how a user will rate a movie they have not yet viewed, based on their historical preferences.""")

            st.write("""### Source:""") 
            st.write("""The data  is maintained by the research team in the Department of Information Techology of the University of Nairobi. Additional movie content data was legally scraped from IMDB""")


            st.write("""### Supplied Files:
                genome_scores.csv - a score mapping the strength between movies and tag-related properties. Read more here

                genome_tags.csv - user assigned tags for genome-related scores

                imdb_data.csv - Additional movie metadata scraped from IMDB using the links.csv file.

                links.csv - File providing a mapping between a MovieLens ID and associated IMDB and TMDB IDs.

                sample_submission.csv - Sample of the submission format for the hackathon.

                tags.csv - User assigned for the movies within the dataset.

                test.csv - The test split of the dataset. Contains user and movie IDs with no rating data.

                train.csv - The training split of the dataset. Contains user and movie IDs with associated rating data.""")

        
	    # Building out the Data  Exploratory page 
    # You may want to add more sections here for aspects such as an EDA,
    # or to provide your business pitch....


if __name__ == '__main__':
    main()
