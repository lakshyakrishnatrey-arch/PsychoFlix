import streamlit as st


def show_home(recommender):

    st.markdown(
        """
        <h1 style='text-align:center;color:#E50914;'>
            🎬 PsychoFlix
        </h1>

        <h4 style='text-align:center;color:white;'>
            AI Powered Psychological Movie Recommendation System
        </h4>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    movie_name = st.selectbox(
    "🔍 Search for a Movie",
    recommender.movie_titles(),
    index=None,
    placeholder="Start typing a movie..."
    )

    if st.button("🎯 Recommend Movies", use_container_width=True):

        if movie_name.strip() == "":
            st.warning("Please enter a movie.")
            return

        recommendations = recommender.recommend(movie_name)

        if recommendations is None or recommendations.empty:
            st.error("Movie not found.")
            return

        st.divider()

        st.subheader("🎬 Recommended Movies")

        for _, row in recommendations.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.markdown(f"## 🎬 {row['title']}")

                with col2:

                    st.metric(
                        "⭐ Rating",
                        round(row["vote_average"], 1)
                    )

                st.write("### 🎭 Genres")

                genre_cols = st.columns(len(row["genres"]))

                for col, genre in zip(genre_cols, row["genres"]):
                    col.success(genre)

                st.write("")

                st.write("### 🧠 Emotional Profile")

                emotion_cols = st.columns(len(row["emotions"]))

                for col, emotion in zip(emotion_cols, row["emotions"]):
                    col.info(emotion)

                st.write("")

                st.caption(
                    f"📅 Released: {str(row['release_date'])[:4]}"
                )

                with st.expander("📝 Read Overview"):

                    st.write(row["overview"])

                st.divider()