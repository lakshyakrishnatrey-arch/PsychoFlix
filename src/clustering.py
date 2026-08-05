import pandas as pd

from collections import Counter

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

        self.cluster_names = self._generate_cluster_names()

    def _generate_cluster_names(self):

        names = {}

        for cluster in sorted(self.movies["Cluster"].unique()):

            cluster_movies = self.movies[
                self.movies["Cluster"] == cluster
            ]

            genres = []

            for g in cluster_movies["genres"]:
                genres.extend(g)

            top = Counter(genres).most_common(2)

            if len(top) >= 2:
                names[cluster] = f"{top[0][0]} & {top[1][0]}"
            elif len(top) == 1:
                names[cluster] = top[0][0]
            else:
                names[cluster] = "Mixed Movies"

        return names

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

    def cluster_name(self, cluster):

        return self.cluster_names.get(
            cluster,
            "Unknown Cluster"
        )