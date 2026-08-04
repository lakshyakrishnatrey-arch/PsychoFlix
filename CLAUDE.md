# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Install dependencies**: `pip install -r requirements.txt`
- **Run app**: `streamlit run app.py`
- **Lint**: `flake8 . --max-line-length=120`
- **Test**: `pytest tests/`
- **Run single test**: `pytest tests/test_recommendations.py`
- **Build analytics**: `python analytics/build.py`

## Architecture Overview

The project follows a modular structure with these key components:

1. **data/**
   - `movies.csv`: Movie metadata including psychological impact tags
   - `user_profiles.csv`: User psychological profiles
   - `ratings.csv`: User ratings for movies

2. **src/**
   - `recommender.py`: Core recommendation engine using data mining techniques
   - `utils.py`: Helper functions for data processing
   - `admin.py`: Admin functionality implementation

3. **app.py**: Streamlit UI main application file
4. **tests/**: Unit tests for recommendation logic
5. **analytics/**: Scripts for data analysis and visualization

## Key Technical Details

- **Recommendation Engine**: Uses collaborative filtering with psychological profile integration
- **UI Components**: Streamlit components for user input, recommendation display, and explanations
- **Analytics**: Includes scripts for generating popularity charts, impact analysis, and user behavior visualizations
- **Admin Features**: User management, movie database updates, and recommendation model retraining capabilities

## Important Files

- `src/recommender.py`: Heart of the recommendation system
- `app.py`: Main entry point for the Streamlit application
- `analytics/visualizations.py`: Contains all visualization code for analytics dashboard
- `config.yaml`: Configuration file for model parameters and database connections