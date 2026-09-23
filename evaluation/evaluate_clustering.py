"""
PsychoFlix - K-Means Clustering Evaluation
============================================
Evaluates K-Means clustering quality across multiple cluster counts:
  K in {5, 7, 10, 12, 15}

Metrics:
  - Silhouette Score: Quality of cluster separation and cohesion [-1, 1]
  - Inertia (WCSS): Within-cluster sum of squares
  - Cluster Purity: Average fraction of movies in each cluster sharing the dominant genre

Implementation details:
  - Uses TF-IDF vectorizer (stop_words='english', max_features=5000) matching MovieCluster
  - KMeans with random_state=42 and n_init=10
  - Does NOT alter production K=10 unless technically justified

No results are fabricated. All values are calculated from the actual dataset.
"""

import sys
import os
import pandas as pd
import numpy as np
from collections import Counter

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
os.chdir(PROJECT_ROOT)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


def evaluate_clustering(k_values=(5, 7, 10, 12, 15), random_state=42):
    print("=" * 60)
    print("PsychoFlix - K-Means Clustering Evaluation")
    print("=" * 60)

    print("\n[1/3] Loading dataset & extracting TF-IDF features...")
    movies = pd.read_pickle("preprocessing/processed_movies.pkl")
    print(f"      Total movies: {len(movies)}")

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000
    )
    matrix = vectorizer.fit_transform(movies["tags"])
    print(f"      TF-IDF matrix shape: {matrix.shape}")

    print(f"\n[2/3] Evaluating K in {list(k_values)} with random_state={random_state}...\n")
    results = []

    for k in k_values:
        print(f"  Testing K = {k:>2d} ... ", end="", flush=True)

        kmeans = KMeans(
            n_clusters=k,
            random_state=random_state,
            n_init=10
        )
        labels = kmeans.fit_predict(matrix)
        inertia = float(kmeans.inertia_)

        # Silhouette score computed on full matrix
        sil = float(silhouette_score(matrix, labels, random_state=random_state))

        # Cluster Purity: for each cluster, calculate the fraction of movies containing its dominant genre
        temp_df = movies.copy()
        temp_df["cluster"] = labels

        purity_list = []
        for c in range(k):
            c_movies = temp_df[temp_df["cluster"] == c]
            if len(c_movies) == 0:
                continue
            all_genres = []
            for g in c_movies["genres"]:
                all_genres.extend(g)
            if not all_genres:
                continue
            top_genre = Counter(all_genres).most_common(1)[0][0]
            hits = c_movies["genres"].apply(lambda glist: top_genre in glist).sum()
            purity_list.append(hits / len(c_movies))

        purity = float(np.mean(purity_list)) if purity_list else 0.0

        print(f"Silhouette: {sil:.4f} | Inertia: {inertia:.1f} | Purity: {purity:.4f}")

        results.append({
            "k": k,
            "silhouette_score": round(sil, 4),
            "inertia": round(inertia, 2),
            "cluster_purity": round(purity, 4),
        })

    results_df = pd.DataFrame(results)

    best_idx = results_df["silhouette_score"].idxmax()
    best_k = int(results_df.loc[best_idx, "k"])
    best_sil = results_df.loc[best_idx, "silhouette_score"]
    current_k_row = results_df[results_df["k"] == 10].iloc[0]
    current_sil = current_k_row["silhouette_score"]

    print(f"\n[3/3] Clustering Summary:")
    print(f"  Current production K = 10 Silhouette Score: {current_sil:.4f}")
    print(f"  Best K by Silhouette Score:                K = {best_k} ({best_sil:.4f})")

    diff = best_sil - current_sil
    if best_k != 10 and diff > 0.05:
        print(f"  NOTE: K={best_k} offers a significant improvement (+{diff:.4f}).")
    else:
        print(f"  NOTE: Difference is marginal ({diff:+.4f}). Retaining current K=10 is technically justified.")

    # Format summary records for evaluation_results.csv
    summary_records = []
    for _, row in results_df.iterrows():
        k = int(row["k"])
        tag = " (current)" if k == 10 else ""
        summary_records.append({
            "component": "Clustering",
            "metric": f"Silhouette Score (K={k}){tag}",
            "value": row["silhouette_score"]
        })
        summary_records.append({
            "component": "Clustering",
            "metric": f"Inertia (K={k}){tag}",
            "value": row["inertia"]
        })
        summary_records.append({
            "component": "Clustering",
            "metric": f"Cluster Purity (K={k}){tag}",
            "value": row["cluster_purity"]
        })

    summary_records.append({
        "component": "Clustering",
        "metric": "Optimal K by Silhouette",
        "value": best_k
    })

    summary = pd.DataFrame(summary_records)

    detail_path = os.path.join(PROJECT_ROOT, "evaluation", "clustering_details.csv")
    results_df.to_csv(detail_path, index=False, encoding="utf-8")
    print(f"  Detailed metrics saved -> {detail_path}\n")

    return summary


if __name__ == "__main__":
    summary_df = evaluate_clustering()
    out_path = os.path.join(PROJECT_ROOT, "evaluation", "evaluation_results.csv")
    if os.path.exists(out_path):
        existing = pd.read_csv(out_path)
        combined = pd.concat([existing, summary_df], ignore_index=True)
        combined.to_csv(out_path, index=False, encoding="utf-8")
    else:
        summary_df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"Results appended -> {out_path}")
