import streamlit as st
import pandas as pd

from src.recommender import Recommender


st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)


@st.cache_data
def load_data():
    movies = pd.read_csv("dataset/movies.csv")
    responses = pd.read_csv("dataset/responses.csv")
    return movies, responses


def main():

    st.markdown("""
    <style>
    .stApp{
        background-color:#121212;
        color:white;
    }

    h1{
        color:#E50914;
        text-align:center;
    }

    h3{
        text-align:center;
        color:white;
    }

    .stButton>button{
        background:#E50914;
        color:white;
        border-radius:10px;
        height:50px;
        width:100%;
        font-size:18px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1>PsychoFlix</h1>
    <h3>AI Powered Psychological Movie Recommender</h3>
    """, unsafe_allow_html=True)

    movies, responses = load_data()

    current_user = st.text_input("Enter your User ID")

    if st.button("Recommend"):

        recommender = Recommender(movies, responses)
        recommendations = recommender.recommend(current_user)

        st.subheader("Recommended Movies")

        if recommendations.empty:
            st.warning("No recommendations found.")

        else:

            for _, row in recommendations.iterrows():

                st.container(border=True)

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### {row['title']}")
                    if "genre" in row:
                        st.write(f"🎭 {row['genre']}")

                with col2:
                    st.write("⭐")


if __name__ == "__main__":
    main()