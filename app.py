import streamlit as st
import plotly.express as px

from src.tmdb_recommender import TMDBRecommender
from src.analytics import MovieAnalytics

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_resource
def load_recommender():
    return TMDBRecommender()

@st.cache_resource
def load_analytics():
    return MovieAnalytics()

recommender = load_recommender()
analytics = load_analytics()

# -------------------------------------------------
# CSS
# -------------------------------------------------

st.markdown("""
<style>

.stApp{
    background:#121212;
    color:white;
}

h1{
    color:#E50914;
    text-align:center;
}

h2{
    color:white;
}

div[data-testid="stSidebar"]{
    background:#1b1b1b;
}

.stButton > button{
    background:#E50914;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
}

.stButton > button:hover{
    background:#B20710;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# SIDEBAR
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

# -------------------------------------------------
# HOME
# -------------------------------------------------

if page == "🏠 Home":

    st.markdown(
        """
        <h1>🎬 PsychoFlix</h1>
        <h3 style="text-align:center;">
        AI Powered Psychological Movie Recommender
        </h3>
        """,
        unsafe_allow_html=True
    )

    movie_name = st.text_input(
        "🔍 Search for a Movie",
        placeholder="Avatar, Interstellar, Inception..."
    )

    if st.button("Recommend"):

        if movie_name.strip() == "":
            st.warning("Please enter a movie.")
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

    st.title("📊 Movie Analytics Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🎬 Total Movies",
            analytics.total_movies()
        )

    with col2:
        st.metric(
            "⭐ Average Rating",
            analytics.average_rating()
        )

    st.divider()

    # Top Rated Movies
    st.subheader("⭐ Top Rated Movies")

    st.dataframe(
        analytics.top_movies(),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Rating Distribution
    st.subheader("📈 Rating Distribution")

    fig = px.histogram(
        x=analytics.ratings(),
        nbins=20,
        labels={"x": "Rating", "y": "Movies"},
        title="Distribution of Movie Ratings"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.divider()

    # Genre Distribution
    st.subheader("🎭 Top 10 Genres")

    genre_counts = analytics.genre_counts().head(10)

    genre_fig = px.bar(
        x=genre_counts.index,
        y=genre_counts.values,
        labels={
            "x": "Genre",
            "y": "Number of Movies"
        },
        title="Top 10 Movie Genres"
    )

    st.plotly_chart(
        genre_fig,
        use_container_width=True
    )

    st.divider()

    # Release Year Trend
    st.subheader("📅 Movies Released Per Year")

    release_data = analytics.release_years()

    release_fig = px.line(
        x=release_data.index,
        y=release_data.values,
        labels={
            "x": "Year",
            "y": "Movies Released"
        },
        title="Movie Release Trend"
    )

    st.plotly_chart(
        release_fig,
        use_container_width=True
    )

# -------------------------------------------------
# MOOD PAGE
# -------------------------------------------------

elif page == "🧠 Mood Recommender":

    st.title("🧠 Mood Based Recommendation")

    mood = st.selectbox(
        "Choose your current mood",
        [
            "😊 Happy",
            "😔 Sad",
            "😌 Relaxed",
            "💪 Motivated",
            "😰 Stressed"
        ]
    )

    st.info(
        "Psychological recommendations based on mood "
        "will be implemented in the next phase."
    )

# -------------------------------------------------
# ABOUT PAGE
# -------------------------------------------------

elif page == "ℹ About":

    st.title("🎬 About PsychoFlix")

    st.write("""
### AI Powered Psychological Movie Recommendation System

PsychoFlix is a Data Mining project that recommends movies
using Machine Learning and content-based filtering.

### Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Scikit-learn
- TF-IDF Vectorization
- Cosine Similarity
- TMDB Dataset

### Dataset

- 4803 Movies
- Content-based Recommendation
- Metadata Analysis

### Upcoming Features

- 🎬 Movie Posters
- 🤖 K-Means Clustering
- 📊 Advanced Dashboard
- 🧠 Psychological Recommendation Engine
- 🎭 Mood Prediction
""")