import streamlit as st

from src.tmdb_recommender import TMDBRecommender

st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)


@st.cache_resource
def load_recommender():
    return TMDBRecommender()


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
        font-size:3.2rem;
    }

    h3{
        text-align:center;
        color:white;
        margin-bottom:30px;
    }

    .stButton>button{
        background:#E50914;
        color:white;
        border-radius:10px;
        height:50px;
        width:100%;
        font-size:18px;
        border:none;
    }

    .stButton>button:hover{
        background:#B20710;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <h1>🎬 PsychoFlix</h1>
    <h3>AI Powered Psychological Movie Recommender</h3>
    """, unsafe_allow_html=True)

    recommender = load_recommender()

    movie_name = st.text_input(
        "🔍 Search for a movie",
        placeholder="Example: Avatar, Interstellar, Inception"
    )

    if st.button("Recommend"):

        if movie_name.strip() == "":
            st.warning("Please enter a movie name.")
            return

        recommendations = recommender.recommend(movie_name)

        if recommendations is None or recommendations.empty:
            st.error("Movie not found. Please check the spelling.")
            return

        st.subheader("🎥 Recommended Movies")

        for i, (_, row) in enumerate(recommendations.iterrows(), start=1):

            with st.container(border=True):

                st.markdown(f"### {i}. {row['title']}")


if __name__ == "__main__":
    main()