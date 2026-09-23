# 🔬 PsychoFlix — Machine Learning Model Evaluation & Validation Report

**Evaluation Date**: 2026-09-24  
**Dataset**: TMDB 5,000 Movies & Credits Dataset (`tmdb_5000_movies.csv`, `tmdb_5000_credits.csv`)  
**Processed Movies**: 4,803 titles  
**Evaluation Standard**: Rigorous, reproducible, zero-fabrication empirical testing (`random_state=42`)

---

## 1. Executive Summary

This report documents the empirical evaluation and technical validation of the three core algorithmic components in the **PsychoFlix** platform:
1. **Content-Based Recommendation Engine** (`TMDBRecommender`): TF-IDF feature extraction on textual metadata tags + Cosine Similarity ranking.
2. **Unsupervised K-Means Clustering** (`MovieCluster`): TF-IDF feature space (5,000 dimensions) with cluster assignment across varying $K \in \{5, 7, 10, 12, 15\}$.
3. **Psychological Mood Recommender** (`MoodRecommender` & `PsychologyEngine`): Rule-based emotion-to-genre heuristic mapping and rating-priority retrieval.

All metrics reported here were generated through execution of scripts in `evaluation/` on the actual dataset and production code.

---

## 2. Recommender Evaluation (TF-IDF + Cosine Similarity)

### 2.1 Methodology & Definition of Relevance
The TMDB 5000 dataset contains static metadata (genres, cast, keywords, directors, overviews, taglines). It does **not** contain user interaction logs, ratings matrices, or explicit pairwise co-watch ground truth. 

To evaluate recommendation performance without fabricating synthetic interactions:
- **Representative Query Sample**: 50 movies were deterministically sampled from the 4,803-movie catalog using `random_state=42`.
- **Top-$N$ Retrieval**: For each query movie, top-5 and top-10 recommendations were generated using the production `TMDBRecommender.recommend()` pipeline.
- **Relevance Definition (Proxy Metric)**: A recommended movie is classified as **Relevant** if and only if it shares at least one genre with the query movie:
  $$\text{Relevant}(q, r) = \mathbb{I}(|\text{Genres}(q) \cap \text{Genres}(r)| \ge 1)$$
- **Precision@K**: The proportion of recommended items in the top-$K$ list that are relevant:
  $$\text{Precision@K} = \frac{1}{|Q|} \sum_{q \in Q} \frac{\sum_{i=1}^K \text{Relevant}(q, r_i)}{K}$$
- **Genre-Overlap Accuracy (Hit Rate)**: The overall hit rate across all retrieved candidate positions:
  $$\text{Accuracy}_{\text{genre}} = \frac{\text{Total Relevant Recommendations Across All Queries}}{\text{Total Recommendations Retained (50 } \times 10 = 500)}$$
- **Confidence Signal**: The mean cosine similarity of the top-10 recommended vectors against the query vector.

### 2.2 Empirical Results

| Metric | Measured Value | Percentage | Description |
| :--- | :--- | :--- | :--- |
| **Genre-Overlap Precision@5** | **0.8280** | **82.80%** | Average precision across top-5 recommendations |
| **Genre-Overlap Precision@10** | **0.8300** | **83.00%** | Average precision across top-10 recommendations |
| **Genre-Overlap Accuracy (Hit Rate)** | **0.8300** | **83.00%** | 415 out of 500 recommendations share $\ge 1$ genre with query |
| **Mean Cosine Similarity (Top-10)** | **0.1260** | — | Average vector similarity score of recommendations |
| **Evaluated Queries ($N$)** | **50** | — | Sample size drawn with `random_state=42` |

### 2.3 Technical Analysis
- The high Precision@10 ($83.00\%$) confirms that the TF-IDF representation of combined tags (genres, keywords, cast, crew, overview) preserves core genre identity without explicit hard filtering.
- The average cosine similarity of $0.1260$ illustrates the sparsity of the 5,000+ token text space. In high-dimensional vocabulary spaces, cosine scores in the $0.10 - 0.25$ range are standard for top document matches.

---

## 3. K-Means Clustering Validation

### 3.1 Methodology
The clustering subsystem partitions the movie space into thematic clusters using TF-IDF vectors (`max_features=5000`, `stop_words='english'`). To assess whether the production cluster count $K=10$ is mathematically sound, five candidate cluster configurations were tested: $K \in \{5, 7, 10, 12, 15\}$, with `random_state=42` and `n_init=10`.

Evaluation metrics:
1. **Silhouette Coefficient**: Measures how well an object lies within its cluster compared to neighboring clusters (range $[-1, 1]$).
2. **Inertia (Within-Cluster Sum of Squares - WCSS)**: Measures cluster compactness (lower is tighter).
3. **Cluster Purity**: The average proportion of movies within each cluster that share the cluster's most frequent genre:
   $$\text{Purity}(C_k) = \frac{\max_{g} |\{m \in C_k : g \in \text{Genres}(m)\}|}{|C_k|}, \quad \text{Overall Purity} = \frac{1}{K} \sum_{k=1}^K \text{Purity}(C_k)$$

### 3.2 Empirical Results

| Number of Clusters ($K$) | Silhouette Score | Inertia (WCSS) | Cluster Purity | Status |
| :---: | :---: | :---: | :---: | :--- |
| **K = 5** | 0.0042 | 4,670.04 | 0.6982 | Tested |
| **K = 7** | 0.0044 | 4,651.56 | 0.7143 | Tested |
| **K = 10** | **0.0052** | **4,630.77** | **0.7495** | **Current Production Choice** |
| **K = 12** | 0.0053 | 4,618.46 | 0.7288 | Tested |
| **K = 15** | 0.0057 | 4,604.00 | 0.7393 | Tested |

### 3.3 Technical Justification of $K=10$
1. **Purity Peak**: $K=10$ attains the **highest cluster purity (74.95%)** among all evaluated configurations. On average, nearly 3 out of 4 movies in any given cluster share the primary genre theme.
2. **Negligible Silhouette Difference**: While $K=15$ yields a silhouette score of $0.0057$ versus $0.0052$ for $K=10$, the difference is an imperceptible $+0.0005$ in sparse text space.
3. **Cognitive Usability**: $10$ clusters map cleanly into human-interpretable category tiles on the Streamlit dashboard without overwhelming users or creating single-movie fragment clusters.
4. **Decision**: **Retaining $K=10$ is fully justified technically and empirically.**

---

## 4. Psychological Mood Recommender Evaluation

### 4.1 Methodology & Definitions
The psychological recommendation engine is governed by `PsychologyEngine.genre_to_emotion`. When a user requests a mood, `MoodRecommender` filters all catalog titles whose derived emotions contain that mood tag, then sorts candidates by audience rating (`vote_average`).

Metrics:
- **Filter Accuracy / Integrity**: Verification that 100% of returned movies contain the requested emotion tag in their profile.
- **Mood Alignment / Relevance Score**: For a movie with genres $G_m$ and target mood $M$ associated with genre set $G_M$:
  $$\text{Alignment}(m, M) = \frac{|G_m \cap G_M|}{|G_m|}$$
  This quantifies whether a movie is purely dedicated to the mood or includes unrelated secondary genres.
- **Catalog Coverage**: Proportion of the 4,803 movies reachable via that mood.
- **Mean Rating**: Average `vote_average` of all qualifying movies.

### 4.2 Empirical Results by Mood

| Mood Target | Supported? | Movie Count | Catalog Coverage | Filter Accuracy | Mood Alignment | Mean Rating |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Happy** (`😊 Happy`) | Yes | 2,499 | 52.03% | 1.0000 | 0.5508 | 6.04 |
| **Sad** (`😢 Sad`) | **No** | 0 | 0.00% | 0.0000 | 0.0000 | N/A |
| **Relaxed** (`😌 Relaxed`) | Yes | 1,961 | 40.83% | 1.0000 | 0.5440 | 5.98 |
| **Motivated** (`💪 Motivated`) | Yes | 1,517 | 31.58% | 1.0000 | 0.4336 | 6.07 |
| **Stressed** (`😫 Stressed`) | **No** | 0 | 0.00% | 0.0000 | 0.0000 | N/A |
| **Reflective** (`🤔 Reflective`) | Yes | 2,323 | 48.37% | 1.0000 | 0.4893 | 6.39 |
| **Escapism** (`🌈 Escapism`) | Yes | 874 | 18.20% | 1.0000 | 0.3513 | 6.07 |
| **Excited** (`⚡ Excited`) | Yes | 1,556 | 32.40% | 1.0000 | 0.4345 | 6.06 |
| **Learning** (`📚 Learning`) | Yes | 301 | 6.27% | 1.0000 | 0.5191 | 6.54 |
| **Romantic** (`❤️ Romantic`) | Yes | 894 | 18.61% | 1.0000 | 0.3843 | 6.21 |
| **Angry** (`😡 Angry`) | Yes | 1,700 | 35.39% | 1.0000 | 0.4093 | 6.14 |
| **Frustrated** (`😤 Frustrated`) | Yes | 3,073 | 63.98% | 1.0000 | 0.5349 | 6.25 |
| **Overall (Supported Moods Avg)** | **Yes** | **1,670** | **34.77%** | **1.0000** | **0.4651** | **6.18** |

### 4.3 Findings Regarding "Sad" and "Stressed"
- **"Sad"** and **"Stressed"** do not exist in the current `genre_to_emotion` ontology in `src/psychology.py`.
- Querying for these moods yields 0 movies (0% coverage).
- In contrast, related emotional states such as `😤 Frustrated` (covers Drama, Mystery, Thriller) and `🤔 Reflective` (covers Drama, War) are well-represented ($63.98\%$ and $48.37\%$ coverage).
- Rather than fabricating synthetic results, this evaluation formally identifies this ontology gap as a key recommendation for future enhancement.

---

## 5. Limitations & Caveats

1. **Proxy vs. True User Relevance**:
   - Genre overlap is a content-coherence proxy, not ground-truth user satisfaction. A user who likes *Inception* (Sci-Fi, Action) might not enjoy all other Sci-Fi Action films.
2. **Text Sparsity in Clustering**:
   - Silhouette scores for TF-IDF on high-dimensional text (5,000 features) are typically low ($0.004 - 0.006$) due to high document sparsity. Density-based or embedding-based clustering (e.g. BERT/SentenceTransformers) could yield tighter clusters.
3. **Rule-Based Psychological Mapping**:
   - Emotions are statically inferred from genre labels alone. Nuance in plot overview, sentiment, tone, and musical score is not captured by this dictionary lookup.
4. **Cold Start & Popularity Bias**:
   - `MoodRecommender` sorts by `vote_average`, creating a mild bias toward movies with high average ratings regardless of how strongly they embody the requested mood.

---

## 6. How to Reproduce All Results

Run each script from the `PsychoFlix/` root directory:

```bash
# 1. Recommender Evaluation
python evaluation/evaluate_recommender.py

# 2. Clustering Evaluation
python evaluation/evaluate_clustering.py

# 3. Mood Recommender Evaluation
python evaluation/evaluate_mood.py

# 4. View Compiled CSV
cat evaluation/evaluation_results.csv
```

All detailed per-query and per-cluster tables are saved to:
- `evaluation/recommender_details.csv`
- `evaluation/clustering_details.csv`
- `evaluation/mood_details.csv`
- `evaluation/evaluation_results.csv`
