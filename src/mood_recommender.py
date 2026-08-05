import pandas as pd

from src.psychology import PsychologyEngine


class MoodRecommender:

    def __init__(self):

        self.movies = pd.read_pickle(
            "preprocessing/processed_movies.pkl"
        )

        self.psychology = PsychologyEngine()

        self.movies["emotions"] = self.movies["genres"].apply(
            self.psychology.emotions_from_genres
        )

    def recommend(self, mood, top_n=10):

        filtered = self.movies[
            self.movies["emotions"].apply(
                lambda emotions: mood in emotions
            )
        ].copy()

        if filtered.empty:
            return None

        filtered["reason"] = (
            "Matches your selected mood • Highly rated movie"
        )

        return (
            filtered
            .sort_values(
                by="vote_average",
                ascending=False
            )
            .head(top_n)
        )