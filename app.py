import streamlit as st
import pandas as pd

from src.recommender import Recommender


@st.cache_data
def load_data():
    movies = pd.read_csv("dataset/movies.csv")
    responses = pd.read_csv("dataset/responses.csv")
    return movies, responses


def main():
    # Custom CSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: white;
    }

    h1 {
        color: #E50914;
        text-align: center;
        font-size: 3rem;
    }

    .stButton > button {
        background-color: #E50914;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        border: none;
    }

    .stButton > button:hover {
        background-color: #B20710;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("🎬 Movie Recommendation System")

    movies, responses = load_data()

    current_user = st.text_input("Enter your User ID")

    if st.button("Recommend"):

        recommender = Recommender(movies, responses)

        recommendations = recommender.recommend(current_user)

        st.subheader("Recommended Movies")

        if recommendations.empty:
            st.warning("No recommendations found.")
        else:
            if "title" in recommendations.columns:
                st.dataframe(recommendations[["title"]])

            elif "Movie Title" in recommendations.columns:
                st.dataframe(recommendations[["Movie Title"]])

            else:
                st.dataframe(recommendations)


if __name__ == "__main__":
    main()