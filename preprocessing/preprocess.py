import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def load_raw_data():
    """Load raw datasets"""
    movies = pd.read_csv('dataset/movies.csv')
    responses = pd.read_csv('dataset/responses.csv')
    return movies, responses


def preprocess_data(movies, responses):
    """Clean and prepare data for recommendations"""
    # Merge datasets
    merged = pd.merge(movies, responses, on='movie_id', how='left')

    # Handle missing values
    merged['rating'] = merged['rating'].fillna(0)
    merged['watched'] = merged['watched'].fillna(False)

    # Feature engineering
    merged['impact_score'] = merged['psychological_impact_tags'].apply(lambda x: len(str(x).split(','))

    # Normalize numerical features
    scaler = StandardScaler()
    merged['rating'] = scaler.fit_transform(merged[['rating']])

    return merged


def save_processed_data(df):
    """Save processed data to CSV"""
    df.to_csv('data/processed_data.csv', index=False)

if __name__ == '__main__':
    movies, responses = load_raw_data()
    processed_data = preprocess_data(movies, responses)
    save_processed_data(processed_data)
    print('Data preprocessing completed successfully.')