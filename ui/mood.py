import streamlit as st


def show_mood(mood_engine):

    st.title("🧠 Psychological Movie Recommender")

    mood = st.selectbox(
        "How are you feeling today?",
        [
            "😊 Happy",
            "😌 Relaxed",
            "💪 Motivated",
            "🤔 Reflective",
            "🌈 Escapism",
            "⚡ Excited",
            "📚 Learning",
            "❤️ Romantic",
            "😡 Angry",
            "😤 Frustrated"
        ]
    )

    if st.button("Recommend for My Mood"):

        recommendations = mood_engine.recommend(mood)

        if recommendations is None or recommendations.empty:

            st.warning(
                "No movies found for this mood."
            )

            return

        st.subheader("🎬 Recommended Movies")

        for _, row in recommendations.iterrows():

            with st.container(border=True):

                st.markdown(
                    f"### 🎬 {row['title']}"
                )

                st.write(
                    f"⭐ Rating: {row['vote_average']}"
                )

                st.write(
                    "🎭 Genres: "
                    + ", ".join(row["genres"])
                )

                st.write(
                    "🧠 Emotional Profile"
                )

                st.success(
                    " | ".join(row["emotions"])
                )

                st.info(
                    row["reason"]
                )

                st.write("📝 Overview")

                st.write(row["overview"])