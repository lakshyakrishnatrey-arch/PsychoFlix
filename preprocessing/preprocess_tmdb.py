import pandas as pd
import ast

# -------------------------------
# Load TMDB datasets
# -------------------------------

movies = pd.read_csv("dataset/tmdb/tmdb_5000_movies.csv")
credits = pd.read_csv("dataset/tmdb/tmdb_5000_credits.csv")

# Rename movie ID column
movies = movies.rename(columns={"id": "movie_id"})

# Merge datasets
merged = pd.merge(movies, credits, on="movie_id")

# Remove rows with missing titles
merged = merged.dropna(subset=["title_x"])


# -------------------------------
# Helper Functions
# -------------------------------

def extract_names(text):
    try:
        data = ast.literal_eval(text)
        return [item["name"] for item in data]
    except:
        return []


def extract_cast(text):
    try:
        data = ast.literal_eval(text)
        return [actor["name"] for actor in data[:5]]
    except:
        return []


def extract_director(text):
    try:
        data = ast.literal_eval(text)
        for member in data:
            if member["job"] == "Director":
                return member["name"]
        return ""
    except:
        return ""


# -------------------------------
# Feature Extraction
# -------------------------------

merged["genres"] = merged["genres"].apply(extract_names)
merged["keywords"] = merged["keywords"].apply(extract_names)
merged["cast"] = merged["cast"].apply(extract_cast)
merged["director"] = merged["crew"].apply(extract_director)

merged["overview"] = merged["overview"].fillna("")
merged["tagline"] = merged["tagline"].fillna("")

# Create tags column
merged["tags"] = merged.apply(
    lambda row: " ".join(
        row["genres"]
        + row["keywords"]
        + row["cast"]
        + [row["director"]]
        + [row["overview"]]
        + [row["tagline"]]
    ),
    axis=1,
)

# -------------------------------
# Save processed dataset
# -------------------------------

processed = merged[
    [
        "movie_id",
        "title_x",
        "genres",
        "vote_average",
        "release_date",
        "overview",
        "tags",
    ]
].rename(columns={"title_x": "title"})

processed.to_pickle("preprocessing/processed_movies.pkl")

print("✅ Preprocessing completed successfully!")
print(f"Movies processed: {len(processed)}")
print("Saved preprocessing/processed_movies.pkl")