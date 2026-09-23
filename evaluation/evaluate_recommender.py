"""
PsychoFlix - Recommender Evaluation
====================================
Evaluates the TF-IDF + Cosine Similarity recommender using
genre-overlap as a transparent relevance proxy.

Metrics:
  - Genre-Overlap Precision@5: Fraction of top-5 recommended movies sharing >= 1 genre with query
  - Genre-Overlap Precision@10: Fraction of top-10 recommended movies sharing >= 1 genre with query
  - Genre-Overlap Accuracy (Hit Rate): Overall percentage of recommendations sharing >= 1 genre
  - Mean Cosine Similarity: Average cosine similarity score of top-10 recommendations

Relevance Definition:
  Ground-truth user ratings/clickstream data are not available in the TMDB 5000 metadata.
  Therefore, relevance is strictly defined as genre coherence (sharing at least one genre
  with the query movie).

No results are fabricated. All metrics are computed by querying TMDBRecommender
with a representative sample of 50 movies (random_state=42).
"""

import sys
import os
import pandas as pd
import numpy as np

# Set standard output encoding safely for Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.tmdb_recommender import TMDBRecommender


def evaluate_recommender(sample_size=50, random_state=42):
    print("=" * 60)
    print("PsychoFlix - Recommender Evaluation")
    print("=" * 60)

    print("\n[1/4] Loading TMDBRecommender...")
    rec = TMDBRecommender()
    movies = rec.movies.copy()
    total_movies = len(movies)
    print(f"      Total dataset size: {total_movies} movies")

    print(f"[2/4] Sampling {sample_size} query movies (random_state={random_state})...")
    sample = movies.sample(n=min(sample_size, total_movies), random_state=random_state)

    print("[3/4] Computing Precision@5, Precision@10, Hit Rate, and Cosine Similarity...\n")

    records = []

    for _, query_row in sample.iterrows():
        title = query_row["title"]
        query_genres = set(query_row["genres"])

        recs = rec.recommend(title, top_n=10)
        if recs is None or recs.empty:
            continue

        relevance_flags = []
        for _, rec_row in recs.iterrows():
            rec_genres = set(rec_row["genres"])
            is_rel = len(query_genres & rec_genres) > 0
            relevance_flags.append(is_rel)

        rel_at_5 = relevance_flags[:5]
        p5 = sum(rel_at_5) / len(rel_at_5) if rel_at_5 else 0.0

        rel_at_10 = relevance_flags[:10]
        p10 = sum(rel_at_10) / len(rel_at_10) if rel_at_10 else 0.0

        # Cosine similarity for top-10
        idx_match = movies[movies["title"].str.lower() == title.lower().strip()].index
        if len(idx_match) > 0:
            idx = idx_match[0]
            scores = list(enumerate(rec.similarity[idx]))
            scores = sorted(scores, key=lambda x: x[1], reverse=True)
            top10_scores = scores[1:11]
            mean_cos = float(np.mean([s[1] for s in top10_scores]))
        else:
            mean_cos = 0.0

        records.append({
            "query_movie": title,
            "query_genres": "|".join(query_row["genres"]),
            "precision_at_5": round(p5, 4),
            "precision_at_10": round(p10, 4),
            "mean_cosine_sim": round(mean_cos, 4),
            "relevant_top5": sum(rel_at_5),
            "relevant_top10": sum(rel_at_10),
        })

    df = pd.DataFrame(records)

    avg_p5 = df["precision_at_5"].mean()
    avg_p10 = df["precision_at_10"].mean()
    avg_cos = df["mean_cosine_sim"].mean()
    total_relevant = df["relevant_top10"].sum()
    total_recs = len(df) * 10
    genre_accuracy = total_relevant / total_recs if total_recs > 0 else 0.0

    print(f"  Sample size evaluated:     {len(df)}")
    print(f"  Mean Precision@5:          {avg_p5:.4f} ({avg_p5*100:.2f}%)")
    print(f"  Mean Precision@10:         {avg_p10:.4f} ({avg_p10*100:.2f}%)")
    print(f"  Genre Overlap Accuracy:    {genre_accuracy:.4f} ({genre_accuracy*100:.2f}%) [hit rate]")
    print(f"  Mean Cosine Similarity:    {avg_cos:.4f}")

    # Summary table format
    summary = pd.DataFrame([
        {"component": "Recommender", "metric": "Genre-Overlap Precision@5", "value": round(avg_p5, 4)},
        {"component": "Recommender", "metric": "Genre-Overlap Precision@10", "value": round(avg_p10, 4)},
        {"component": "Recommender", "metric": "Genre-Overlap Accuracy (Hit Rate)", "value": round(genre_accuracy, 4)},
        {"component": "Recommender", "metric": "Mean Cosine Similarity (top-10)", "value": round(avg_cos, 4)},
        {"component": "Recommender", "metric": "Sample Size (queries)", "value": len(df)},
    ])

    detail_path = os.path.join(PROJECT_ROOT, "evaluation", "recommender_details.csv")
    df.to_csv(detail_path, index=False, encoding="utf-8")
    print(f"\n[4/4] Details saved -> {detail_path}")
    print("Recommender evaluation complete.\n")

    return summary


if __name__ == "__main__":
    summary_df = evaluate_recommender()
    out_path = os.path.join(PROJECT_ROOT, "evaluation", "evaluation_results.csv")
    summary_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Results saved -> {out_path}")
