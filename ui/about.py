import streamlit as st


def show_about():

    st.title("🎬 About PsychoFlix")

    st.write("""
### AI Powered Psychological Movie Recommendation System

PsychoFlix is a Data Mining and Machine Learning project
that recommends movies using Content-Based Filtering
and Psychological Analysis.

---

### Technologies Used

- Python
- Streamlit
- Pandas
- Scikit-learn
- Plotly
- TF-IDF Vectorization
- Cosine Similarity
- K-Means Clustering

---

### Features

✅ Content-Based Recommendation

✅ Psychological Recommendation

✅ Movie Analytics Dashboard

✅ K-Means Clustering

✅ Mood Detection

---

### Future Improvements

- Movie Posters
- Explainable AI
- Hybrid Recommendation
- User Profiles
- Watchlist
- Deployment
""")