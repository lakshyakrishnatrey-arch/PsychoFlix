import pandas as pd


class MovieAnalytics:

    def __init__(self):
        self.movies = pd.read_pickle(
            "preprocessing/processed_movies.pkl"
        )

    def total_movies(self):
        return len(self.movies)

    def average_rating(self):
        return round(
            self.movies["vote_average"].mean(),
            2
        )

    def top_movies(self, n=10):
        return (
            self.movies
            .sort_values(
                by="vote_average",
                ascending=False
            )
            [["title", "vote_average"]]
            .head(n)
        )

    def genre_counts(self):

        genres = self.movies["genres"].explode()

        return genres.value_counts()

    def ratings(self):
        return self.movies["vote_average"]

    def release_years(self):

        years = pd.to_datetime(
            self.movies["release_date"],
            errors="coerce"
        ).dt.year

        return years.value_counts().sort_index()