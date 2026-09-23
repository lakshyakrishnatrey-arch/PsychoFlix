# 🎬 PsychoFlix

> **AI-Powered Psychological Movie Recommendation System**

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?style=for-the-badge&logo=scikitlearn)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-3F4F75?style=for-the-badge&logo=plotly)

---

## 📖 Overview

PsychoFlix is an AI-powered movie recommendation system developed using **Python**, **Machine Learning**, and **Data Mining** techniques. It recommends movies based on content similarity while also providing psychological and mood-based recommendations through an interactive dashboard.

The project combines recommendation algorithms with data visualization to create a user-friendly movie discovery platform.

---

## ✨ Features

- 🎬 Content-Based Movie Recommendation
- 🧠 Psychological Emotion Mapping
- 🎭 Mood-Based Recommendations
- 📊 Analytics Dashboard
- 🤖 K-Means Movie Clustering
- 📈 Interactive Charts
- 🔍 Searchable Movie Selection
- 🎨 Modern Streamlit Interface

---

## 🛠️ Tech Stack

| Category | Technology |
|-----------|------------|
| Language | Python |
| Framework | Streamlit |
| Machine Learning | Scikit-learn |
| Data Analysis | Pandas, NumPy |
| Visualization | Plotly |
| Recommendation | TF-IDF + Cosine Similarity |
| Clustering | K-Means |
| Dataset | TMDB 5000 Movies |

---

## 🧠 Recommendation Workflow

```text
User Selects a Movie
        │
        ▼
TMDB Dataset
        │
        ▼
Data Preprocessing
        │
        ▼
TF-IDF Vectorization
        │
        ▼
Cosine Similarity
        │
        ▼
Psychological Analysis
        │
        ▼
Recommended Movies
```

---

## 📌 Main Modules

- 🏠 Home
- 📊 Analytics Dashboard (with Model Evaluation & Validation)
- 🧠 Mood Recommender
- ℹ️ About

---

## 📐 Machine Learning Model Evaluation & Validation

PsychoFlix implements an empirical evaluation and validation system adhering strictly to scientific transparency: **zero fabrication**, reproducible sampling (`random_state=42`), and clear proxy definitions where ground-truth interaction logs are absent.

### 1. Content-Based Recommender (TF-IDF + Cosine Similarity)
- **Methodology**: Evaluated on 50 representative movies sampled deterministically from the 4,803-movie catalog (`random_state=42`).
- **Relevance Definition (Proxy)**: A recommendation is considered relevant if it shares $\ge 1$ genre with the query movie ($\text{Relevant}(q, r) = \mathbb{I}(|\text{Genres}(q) \cap \text{Genres}(r)| \ge 1)$).
- **Actual Measured Results**:
  - **Genre-Overlap Precision@5**: **82.80%** (0.8280)
  - **Genre-Overlap Precision@10**: **83.00%** (0.8300)
  - **Genre-Overlap Accuracy (Hit Rate)**: **83.00%** (415 relevant / 500 recommendation slots)
  - **Mean Cosine Similarity (Top-10)**: **0.1260**

### 2. Unsupervised K-Means Clustering Validation
- **Methodology**: Tested candidate values $K \in \{5, 7, 10, 12, 15\}$ on 5,000-dimensional TF-IDF feature space (`stop_words='english'`) with `random_state=42`.
- **Actual Measured Results**:
  | Clusters ($K$) | Silhouette Score | Inertia (WCSS) | Cluster Purity |
  | :---: | :---: | :---: | :---: |
  | $K=5$ | 0.0042 | 4,670.04 | 69.82% |
  | $K=7$ | 0.0044 | 4,651.56 | 71.43% |
  | **$K=10$ (Current)** | **0.0052** | **4,630.77** | **74.95% (Peak)** |
  | $K=12$ | 0.0053 | 4,618.46 | 72.88% |
  | $K=15$ | 0.0057 | 4,604.00 | 73.93% |
- **Technical Justification**: Current $K=10$ achieves the highest cluster purity (74.95%). The silhouette score difference with $K=15$ is negligible (+0.0005) in high-dimensional text space, justifying retention of $K=10$ for balanced clustering and UI usability.

### 3. Psychological Mood Recommender Validation
- **Methodology**: Evaluates rule-based heuristic mapping across emotional profiles. Measures **Mood Alignment Score** (proportion of candidate's genres matching the mood) and **Catalog Coverage**.
- **Actual Measured Results**:
  | Mood | Supported? | Movie Count | Coverage | Filter Accuracy | Mood Alignment | Mean Rating |
  | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
  | **Happy** (`😊 Happy`) | Yes | 2,499 | 52.03% | 1.0000 | 0.5508 | 6.04 |
  | **Sad** (`😢 Sad`) | **No (Unmapped)** | 0 | 0.00% | 0.0000 | 0.0000 | N/A |
  | **Relaxed** (`😌 Relaxed`) | Yes | 1,961 | 40.83% | 1.0000 | 0.5440 | 5.98 |
  | **Motivated** (`💪 Motivated`) | Yes | 1,517 | 31.58% | 1.0000 | 0.4336 | 6.07 |
  | **Stressed** (`😫 Stressed`) | **No (Unmapped)** | 0 | 0.00% | 0.0000 | 0.0000 | N/A |
  | **Reflective** (`🤔 Reflective`) | Yes | 2,323 | 48.37% | 1.0000 | 0.4893 | 6.39 |
  | **Frustrated** (`😤 Frustrated`) | Yes | 3,073 | 63.98% | 1.0000 | 0.5349 | 6.25 |
  | **Overall (Supported Average)** | Yes | 1,670 | 34.77% | 1.0000 | 0.4651 | 6.18 |

---

## ⚠️ Transparent Limitations

1. **Proxy Metric vs. User Satisfaction**: The TMDB 5000 dataset contains static metadata rather than real-time user ratings or click logs. Genre overlap measures content coherence, not personal user enjoyment.
2. **Text Sparsity in Clustering**: High dimensionality (5,000 vocabulary tokens) causes low silhouette scores across all $K$ values. Future iterations could benefit from dense vector embeddings (e.g. BERT/Sentence-Transformers).
3. **Heuristic Mood Ontology**: Emotional profiles are assigned strictly via genre tags without NLP sentiment analysis on screenplays or user reviews.
4. **Taxonomy Gaps**: "Sad" and "Stressed" are not mapped in the current `PsychologyEngine` dictionary (0% coverage), indicating room for ontology expansion.

---

## 🚀 Running the Project & Reproducing Evaluation

### 1. Run the Streamlit Application
```bash
streamlit run app.py
```

### 2. Reproduce All ML Evaluations
```bash
# Evaluate Recommender Precision & Accuracy
python evaluation/evaluate_recommender.py

# Evaluate K-Means Clustering across K={5, 7, 10, 12, 15}
python evaluation/evaluate_clustering.py

# Evaluate Mood Engine Alignment & Coverage
python evaluation/evaluate_mood.py
```
Output results and details will be saved to `evaluation/evaluation_results.csv` and summarized in `evaluation/EVALUATION_REPORT.md`.

