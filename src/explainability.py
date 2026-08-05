class ExplainabilityEngine:

    def explain(self, searched_movie, recommended_movie):

        reasons = []

        # Shared Genres
        shared_genres = list(
            set(searched_movie["genres"]) &
            set(recommended_movie["genres"])
        )

        if shared_genres:
            reasons.append(
                "🎭 Shares genres: "
                + ", ".join(shared_genres)
            )

        # Shared Emotions
        shared_emotions = list(
            set(searched_movie["emotions"]) &
            set(recommended_movie["emotions"])
        )

        if shared_emotions:
            reasons.append(
                "🧠 Similar emotional profile"
            )

        # Highly Rated
        if recommended_movie["vote_average"] >= 8:
            reasons.append(
                "⭐ Highly rated by audiences"
            )

        # Default
        if not reasons:
            reasons.append(
                "🎬 Similar movie based on content analysis"
            )

        return reasons
    