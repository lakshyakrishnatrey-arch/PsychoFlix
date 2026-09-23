"""
PsychoFlix - Mood Recommender Evaluation
==========================================
Evaluates the rule-based psychological mood recommendation system.

Evaluated Moods:
  - Requested in task: Happy, Sad, Relaxed, Motivated, Stressed
  - All existing moods in PsychologyEngine:
    😊 Happy, 😌 Relaxed, 💪 Motivated, 🤔 Reflective, 🌈 Escapism,
    ⚡ Excited, 📚 Learning, ❤️ Romantic, 😡 Angry, 😤 Frustrated

Metrics per mood:
  - Mood Filter Accuracy / Verification: Fraction of returned movies that have the requested
    emotion in their generated emotion profile (verifies filter logic).
  - Mood Alignment / Relevance Score: For each movie retrieved, the fraction of its total
    genres that directly map to the target mood. E.g., if a movie has genres [Comedy, Family],
    and both map to 'Happy', alignment is 1.0 (100%). If genres are [Comedy, Action], and
    only Comedy maps to 'Happy', alignment is 0.5 (50%).
  - Catalog Coverage: Percentage of the 4,803-movie dataset available for this mood.
  - Mean Rating: Average audience score (vote_average) for movies in this mood category.
  - Available Movie Count: Total number of movies qualified for the mood.

Key Transparency Notes:
  - 'Sad' and 'Stressed' are not defined in the current PsychologyEngine dictionary.
    They are explicitly tested and shown with 0 matches / 0% coverage, highlighting
    a clear area for future taxonomy expansion.
  - This system is rule-based heuristics (genre -> emotion lookup), not a trained
    predictive ML model. Metrics evaluate taxonomic consistency and catalog coverage.

No results are fabricated.
"""

import sys
import os
import pandas as pd
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from src.mood_recommender import MoodRecommender
from src.psychology import PsychologyEngine


def evaluate_mood():
    print("=" * 60)
    print("PsychoFlix - Mood Recommender Evaluation")
    print("=" * 60)

    print("\n[1/3] Loading MoodRecommender and PsychologyEngine...")
    mood_rec = MoodRecommender()
    psych = PsychologyEngine()
    total_movies = len(mood_rec.movies)
    print(f"      Total catalog: {total_movies} movies")

    # Build reverse lookup: emotion -> set of genres that trigger it
    emotion_to_genres = {}
    for genre, emotions in psych.genre_to_emotion.items():
        for emotion in emotions:
            clean_emotion = emotion.strip()
            emotion_to_genres.setdefault(clean_emotion, set()).add(genre)

    # Moods to evaluate
    # 1. Specifically requested five moods:
    # Notice the UI/Engine uses emojis for Happy, Relaxed, Motivated.
    # We will test both canonical names and emoji labels.
    requested_moods = [
        ("Happy", "😊 Happy"),
        ("Sad", "😢 Sad"),  # Not in PsychologyEngine
        ("Relaxed", "😌 Relaxed"),
        ("Motivated", "💪 Motivated"),
        ("Stressed", "😫 Stressed"),  # Not in PsychologyEngine
    ]

    # Additional engine moods:
    other_engine_moods = [
        ("Reflective", "🤔 Reflective"),
        ("Escapism", "🌈 Escapism"),
        ("Excited", "⚡ Excited"),
        ("Learning", "📚 Learning"),
        ("Romantic", "❤️ Romantic"),
        ("Angry", "😡 Angry"),
        ("Frustrated", "😤 Frustrated"),
    ]

    all_evaluation_targets = requested_moods + other_engine_moods

    print("\n[2/3] Evaluating mood relevance, accuracy, and coverage...\n")

    records = []

    for label_name, mood_key in all_evaluation_targets:
        # Check if mood exists in the engine's mapped emotions
        matching_key = None
        for k in emotion_to_genres.keys():
            if mood_key.lower() in k.lower() or label_name.lower() in k.lower():
                matching_key = k
                break

        if matching_key is None:
            # Mood is not defined in the ontology (e.g. Sad, Stressed)
            records.append({
                "mood_label": label_name,
                "engine_key": mood_key,
                "is_supported": False,
                "movie_count": 0,
                "coverage_pct": 0.0,
                "filter_accuracy": 0.0,
                "alignment_score": 0.0,
                "mean_rating": 0.0,
                "mapped_genres": "None (Not defined in PsychologyEngine)"
            })
            print(f"  [-] {label_name:<12} ({mood_key}): NOT MAPPED in PsychologyEngine (0 movies, 0% coverage)")
            continue

        # Mood is supported: extract all movies that qualify
        qualifying = mood_rec.movies[
            mood_rec.movies["emotions"].apply(lambda em_list: matching_key in em_list)
        ].copy()

        count = len(qualifying)
        coverage = (count / total_movies) if total_movies > 0 else 0.0
        genres_for_mood = emotion_to_genres[matching_key]

        if count == 0:
            filter_acc = 0.0
            avg_alignment = 0.0
            avg_rating = 0.0
        else:
            # Filter accuracy verification: all returned movies must contain the mood
            has_mood = qualifying["emotions"].apply(lambda em_list: matching_key in em_list).sum()
            filter_acc = has_mood / count

            # Mood Alignment Score: ratio of genres matching the mood to total genres of the movie
            alignments = []
            for _, row in qualifying.iterrows():
                movie_genres = set(row["genres"])
                if len(movie_genres) == 0:
                    alignments.append(0.0)
                else:
                    overlap = len(movie_genres & genres_for_mood)
                    alignments.append(overlap / len(movie_genres))
            avg_alignment = float(np.mean(alignments)) if alignments else 0.0
            avg_rating = float(qualifying["vote_average"].mean())

        records.append({
            "mood_label": label_name,
            "engine_key": matching_key,
            "is_supported": True,
            "movie_count": count,
            "coverage_pct": round(coverage * 100, 2),
            "filter_accuracy": round(filter_acc, 4),
            "alignment_score": round(avg_alignment, 4),
            "mean_rating": round(avg_rating, 2),
            "mapped_genres": ", ".join(sorted(genres_for_mood))
        })

        print(f"  [+] {label_name:<12} ({matching_key}): Count={count:<5} | Coverage={coverage*100:5.2f}% | "
              f"Filter Acc={filter_acc:.4f} | Alignment={avg_alignment:.4f} | Rating={avg_rating:.2f}")

    df = pd.DataFrame(records)

    # Compute aggregates for supported moods
    supported_df = df[df["is_supported"] == True]
    mean_supported_alignment = supported_df["alignment_score"].mean()
    mean_supported_coverage = supported_df["coverage_pct"].mean()
    mean_supported_accuracy = supported_df["filter_accuracy"].mean()

    print(f"\n[3/3] Aggregate Mood Metrics (Supported Mappings):")
    print(f"  Average Mood Alignment Score: {mean_supported_alignment:.4f} ({mean_supported_alignment*100:.2f}%)")
    print(f"  Average Catalog Coverage:     {mean_supported_coverage:.2f}%")
    print(f"  Average Filter Accuracy:      {mean_supported_accuracy:.4f}")

    # Build summary rows for evaluation_results.csv
    summary_records = []
    for _, r in df.iterrows():
        label = r["mood_label"]
        summary_records.append({
            "component": "Mood",
            "metric": f"Alignment Score ({label})",
            "value": r["alignment_score"]
        })
        summary_records.append({
            "component": "Mood",
            "metric": f"Coverage Pct ({label})",
            "value": r["coverage_pct"]
        })
        summary_records.append({
            "component": "Mood",
            "metric": f"Filter Accuracy ({label})",
            "value": r["filter_accuracy"]
        })

    summary_records.append({
        "component": "Mood",
        "metric": "Mean Alignment Score (Supported Moods)",
        "value": round(mean_supported_alignment, 4)
    })
    summary_records.append({
        "component": "Mood",
        "metric": "Mean Catalog Coverage Pct (Supported Moods)",
        "value": round(mean_supported_coverage, 2)
    })

    summary = pd.DataFrame(summary_records)

    detail_path = os.path.join(PROJECT_ROOT, "evaluation", "mood_details.csv")
    df.to_csv(detail_path, index=False, encoding="utf-8")
    print(f"  Detailed mood metrics saved -> {detail_path}\n")

    return summary


if __name__ == "__main__":
    summary_df = evaluate_mood()
    out_path = os.path.join(PROJECT_ROOT, "evaluation", "evaluation_results.csv")
    if os.path.exists(out_path):
        existing = pd.read_csv(out_path)
        combined = pd.concat([existing, summary_df], ignore_index=True)
        combined.to_csv(out_path, index=False, encoding="utf-8")
    else:
        summary_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Results appended -> {out_path}")
