import streamlit as st


def show_home(recommender):

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

                st.write(
                    "🎭 **Genres:** "
                    + ", ".join(row["genres"])
                )

                year = str(row["release_date"])[:4]

                st.write(
                    f"📅 **Release Year:** {year}"
                )

                st.write("🧠 **Emotional Profile**")

                st.success(
                    " | ".join(row["emotions"])
                )

                st.write("📝 **Overview**")

                st.write(row["overview"])