import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class DataUtils:
    @staticmethod
    def load_data(movie_path, user_path):
        movies = pd.read_csv(movie_path)
        users = pd.read_csv(user_path)
        return movies, users

    @staticmethod
    def explain_recommendation(movie_profile, user_profile):
        explanation = "Based on your psychological profile indicating {} and movie content related to {}...".format(
            ', '.join(user_profile.dropna()),
            ', '.join(movie_profile.dropna())
        )
        return explanation

    @staticmethod
    def get_presentation_name(movie_row):
        return f"{movie_row['title']} ({movie_row['year']}) - {movie_row['genre']}"