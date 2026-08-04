import pandas as pd
import hashlib

class AdminManager:
    def __init__(self, user_data_path, movie_data_path):
        self.user_data_path = user_data_path
        self.movie_data_path = movie_data_path
        self.users = pd.read_csv(user_data_path)
        self.movies = pd.read_csv(movie_data_path)

    def add_user(self, user_id, name, email, psychological_profile):
        new_user = pd.DataFrame([{
            'id': user_id,
            'name': name,
            'email': email,
            'anxiety_relief': psychological_profile.get('anxiety_relief', 0),
            'stress_reduction': psychological_profile.get('stress_reduction', 0),
            'mood_improvement': psychological_profile.get('mood_improvement', 0),
            'emotional_intelligence': psychological_profile.get('emotional_intelligence', 0)
        }])
        self.users = pd.concat([self.users, new_user], ignore_index=True)
        self.save_users()
        return True

    def update_movie_database(self, new_movie_data):
        self.movies = pd.concat([self.movies, pd.DataFrame(new_movie_data)], ignore_index=True)
        self.save_movies()
        return True

    def save_users(self):
        self.users.to_csv(self.user_data_path, index=False)

    def save_movies(self):
        self.movies.to_csv(self.movie_data_path, index=False)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()