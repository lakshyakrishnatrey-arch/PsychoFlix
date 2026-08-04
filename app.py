import streamlit as st
from src.tmdb_recommender import TMDBRecommender

# ----------------------------
# Page Config
# ----------------------------

st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------
# Load Recommender
# ----------------------------

@st.cache_resource
def load_recommender():
    return TMDBRecommender()

# ----------------------------
# Main App
# ----------------------------

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

    .stButton > button{
        background-color:#E50914;
        color:white;
        border:none;
        border-radius:10px;
        height:50px;
        font-size:18px;
        width:100%;
    }

    .stButton > button:hover{
        background-color:#B20710;
    }

    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        """
        <h1>🎬 PsychoFlix</h1>
        <h3>AI Powered Psychological Movie Recommender</h3>
        """,
        unsafe_allow_html=True
    )

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
            st.error("Movie not found.")
            return

        st.subheader("🎥 Recommended Movies")

        for _, row in recommendations.iterrows():

            with st.container(border=True):

                st.markdown(f"## 🎬 {row['title']}")

                st.write(f"⭐ **Rating:** {row['vote_average']}")

                genres = ", ".join(row["genres"])
                st.write(f"🎭 **Genres:** {genres}")

                year = str(row["release_date"])[:4]
                st.write(f"📅 **Release Year:** {year}")

                st.write("📝 **Overview**")

                st.write(row["overview"])

                st.divider()


if __name__ == "__main__":
    main()