import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class MovieCluster:

    def __init__(self):

        self.movies = pd.read_pickle(
            "preprocessing/processed_movies.pkl"
        )

        vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=5000
        )

        matrix = vectorizer.fit_transform(
            self.movies["tags"]
        )

        self.model = KMeans(
            n_clusters=10,
            random_state=42,
            n_init=10
        )

        self.movies["Cluster"] = self.model.fit_predict(
            matrix
        )

    def cluster_counts(self):

        return (
            self.movies["Cluster"]
            .value_counts()
            .sort_index()
        )

    def movies_in_cluster(self, cluster):

        return self.movies[
            self.movies["Cluster"] == cluster
        ][
            [
                "title",
                "vote_average"
            ]
        ].sort_values(
            by="vote_average",
            ascending=False
        )