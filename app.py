import streamlit as st

from src.tmdb_recommender import TMDBRecommender
from src.analytics import MovieAnalytics
from src.clustering import MovieCluster
from src.mood_recommender import MoodRecommender

from ui.home import show_home
from ui.analytics import show_analytics
from ui.mood import show_mood
from ui.about import show_about


# ------------------------------------------
# PAGE CONFIG
# ------------------------------------------

st.set_page_config(
    page_title="PsychoFlix",
    page_icon="🎬",
    layout="wide"
)


# ------------------------------------------
# LOAD MODELS
# ------------------------------------------

@st.cache_resource
def load_recommender():
    return TMDBRecommender()


@st.cache_resource
def load_analytics():
    return MovieAnalytics()


@st.cache_resource
def load_cluster():
    return MovieCluster()


@st.cache_resource
def load_mood():
    return MoodRecommender()


recommender = load_recommender()
analytics = load_analytics()
cluster = load_cluster()
mood_engine = load_mood()


# ------------------------------------------
# CSS
# ------------------------------------------

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

div[data-testid="stSidebar"]{
    background:#1B1B1B;
}

.stButton>button{
    background:#E50914;
    color:white;
    border:none;
    border-radius:10px;
    height:50px;
    width:100%;
    font-size:18px;
}

</style>
""", unsafe_allow_html=True)
# ------------------------------------------
# SIDEBAR
# ------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📊 Analytics",
        "🧠 Mood Recommender",
        "ℹ️ About"
    ]
)

# ------------------------------------------
# ROUTING
# ------------------------------------------

if page == "🏠 Home":
    show_home(recommender)

elif page == "📊 Analytics":
    show_analytics(
        analytics,
        cluster
    )

elif page == "🧠 Mood Recommender":
    show_mood(
        mood_engine
    )

elif page == "ℹ️ About":
    show_about()