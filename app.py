import streamlit as st
from src.tmdb_recommender import TMDBRecommender

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------------------------
# Load Recommendation Engine
# -------------------------------------------------

@st.cache_resource
def load_recommender():
    return TMDBRecommender()


# -------------------------------------------------
# Custom CSS
# -------------------------------------------------

st.markdown("""
<style>

.stApp{
    background-color:#121212;
    color:white;
}

h1{
    color:#E50914;
    text-align:center;
    font-size:3rem;
}

h3{
    text-align:center;
    color:white;
}

div[data-testid="stSidebar"]{
    background:#1A1A1A;
}

.stButton>button{
    background:#E50914;
    color:white;
    border-radius:10px;
    border:none;
    height:50px;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Analytics",
        "🧠 Mood Recommender",
        "ℹ About"
    ]
)

recommender = load_recommender()

# -------------------------------------------------
# HOME PAGE
# -------------------------------------------------

if page == "🏠 Home":

    st.markdown(
        """
        <h1>🎬 PsychoFlix</h1>
        <h3>AI Powered Psychological Movie Recommender</h3>
        """,
        unsafe_allow_html=True
    )

    movie_name = st.text_input(
        "🔍 Search a Movie",
        placeholder="Avatar, Interstellar, Inception..."
    )

    if st.button("Recommend"):

        if movie_name.strip() == "":
            st.warning("Please enter a movie name.")
            st.stop()

        recommendations = recommender.recommend(movie_name)

        if recommendations is None or recommendations.empty:
            st.error("Movie not found.")
            st.stop()

        st.subheader("🎥 Recommended Movies")

        for _, row in recommendations.iterrows():

            with st.container(border=True):

                st.markdown(f"## 🎬 {row['title']}")

                st.write(
                    f"⭐ **Rating:** {row['vote_average']}"
                )

                genres = ", ".join(row["genres"])

                st.write(
                    f"🎭 **Genres:** {genres}"
                )

                year = str(row["release_date"])[:4]

                st.write(
                    f"📅 **Release Year:** {year}"
                )

                st.write("📝 **Overview**")

                st.write(row["overview"])

# -------------------------------------------------
# ANALYTICS PAGE
# -------------------------------------------------

elif page == "📊 Analytics":

    st.title("📊 Movie Analytics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Movies",
            len(recommender.movies)
        )

    with col2:
        st.metric(
            "Average Rating",
            round(
                recommender.movies["vote_average"].mean(),
                2
            )
        )

    st.divider()

    st.write(
        "Analytics dashboard will be added in the next phase."
    )

# -------------------------------------------------
# MOOD PAGE
# -------------------------------------------------

elif page == "🧠 Mood Recommender":

    st.title("🧠 Mood Recommender")

    mood = st.selectbox(
        "Choose your mood",
        [
            "Happy",
            "Sad",
            "Motivated",
            "Relaxed",
            "Stressed"
        ]
    )

    st.info(
        f"Mood-based recommendations for **{mood}** will be implemented in the next phase."
    )

# -------------------------------------------------
# ABOUT PAGE
# -------------------------------------------------

elif page == "ℹ About":

    st.title("About PsychoFlix")

    st.write("""
PsychoFlix is an AI-powered movie recommendation system built using Data Mining and Machine Learning techniques.

Current technologies:

- TMDB Dataset
- Data Preprocessing
- TF-IDF
- Cosine Similarity
- Streamlit

Upcoming features:

- Movie Posters
- K-Means Clustering
- Analytics Dashboard
- Psychological Recommendation Engine
- Mood Detection
""")