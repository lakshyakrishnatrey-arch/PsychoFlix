import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    def __init__(self, movies, responses):
        self.movies = movies
        self.responses = responses

        # Create TF-IDF vectors from psychological tags
        self.vectorizer = TfidfVectorizer()
        self.movie_vectors = self.vectorizer.fit_transform(
            self.movies["psychological_impact_tags"].fillna("")
        )

    def recommend(self, user_id, top_n=5):
        try:
            user_id = int(user_id)

            # Get movies already rated by this user
            user_movies = self.responses[
                self.responses["user_id"] == user_id
            ]["movie_id"].tolist()

            # If user has never rated anything
            if len(user_movies) == 0:
                return self.movies.head(top_n)

            # Use the first liked movie as reference
            movie_id = user_movies[0]

            movie_index = self.movies.index[
                self.movies["movie_id"] == movie_id
            ][0]

            similarity = cosine_similarity(
                self.movie_vectors[movie_index],
                self.movie_vectors
            ).flatten()

            similar_indices = similarity.argsort()[::-1]

            recommendations = []

            for idx in similar_indices:
                current_movie = self.movies.iloc[idx]

                if current_movie["movie_id"] not in user_movies:
                    recommendations.append(current_movie)

                if len(recommendations) == top_n:
                    break

            if len(recommendations) == 0:
                return self.movies.head(top_n)

            return pd.DataFrame(recommendations)

        except Exception:
            return self.movies.head(top_n)