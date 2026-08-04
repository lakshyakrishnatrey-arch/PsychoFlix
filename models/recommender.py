import pandas as pd
import numpy as np

class Recommender:
    def __init__(self, movies_path, users_path, ratings_path):
        self.movies = pd.read_csv(movies_path)
        self.users = pd.read_csv(users_path)
        self.ratings = pd.read_csv(ratings_path)
        self.user_item_matrix = self._create_user_item_matrix()
        self.similarity_matrix = self._compute_similarity()

    def _create_user_item_matrix(self):
        # Create a matrix of user ratings for movies
        matrix = pd.pivot_table(self.ratings, values='rating',
                              index='user_id',
                              columns='movie_id')
        return matrix.fillna(0)

    def _compute_similarity(self):
        # Compute pairwise cosine similarity between users
        user_vectors = self.user_item_matrix.values
        dot_products = np.dot(user_vectors, user_vectors.T)
        norms = np.linalg.norm(user_vectors, axis=1)
        cosine_similarities = dot_products / np.outer(norms, norms)
        return pd.DataFrame(cosine_similarities,
                          index=self.user_item_matrix.index,
                          columns=self.user_item_matrix.index)

    def recommend(self, user_id, n_recommendations=5):
        # Get similarity scores for the target user
        user_similarities = self.similarity_matrix[user_id].drop(user_id).sort_values(ascending=False)

        # Select top 10 similar users
        similar_users = user_similarities.head(10).index.tolist()

        # Aggregate ratings from similar users
        similar_user_ratings = self.user_item_matrix.loc[similar_users]
        aggregated_ratings = similar_user_ratings.sum(axis=0)

        # Filter out movies the user has already rated
        user_rated_movies = self.ratings[self.ratings['user_id'] == user_id]['movie_id']
        valid_movies = aggregated_ratings[~aggregated_ratings.index.isin(user_rated_movies)]

        # Return top N movies by aggregated rating
        return valid_movies.nlargest(n_recommendations, 'rating')