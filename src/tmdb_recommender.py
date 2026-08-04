import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TMDBRecommender:

    def __init__(self):

        self.movies = pd.read_pickle(
            "preprocessing/processed_movies.pkl"
        )

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.matrix = self.vectorizer.fit_transform(
            self.movies["tags"]
        )

        self.similarity = cosine_similarity(self.matrix)

    def recommend(self, movie_title, top_n=10):

        movie_title = movie_title.lower().strip()

        matches = self.movies[
            self.movies["title"].str.lower() == movie_title
        ]

        if matches.empty:
            return None

        idx = matches.index[0]

        scores = list(enumerate(self.similarity[idx]))

        scores = sorted(
            scores,
            key=lambda x: x[1],
            reverse=True
        )

        scores = scores[1:top_n + 1]

        movie_indices = [i[0] for i in scores]

        return self.movies.iloc[movie_indices][
            [
                "title",
                "genres",
                "vote_average",
                "release_date",
                "overview"
            ]
        ]