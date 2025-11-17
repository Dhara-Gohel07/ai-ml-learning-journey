import sys
import os
import pandas as pd

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT, "src"))

from src.preprocessing import preprocess_dataframe
from src.embeddings import load_embedding_model, generate_embeddings
from src.clustering import run_kmeans, run_dbscan, attach_cluster_labels
from src.visualization import plot_tsne
from src.summarizer import summarize_clusters

# Load dataset
df = pd.read_csv("social_media_posts.csv")

# Preprocessing
df = preprocess_dataframe(df)

# Embeddings
model = load_embedding_model()
embeddings = generate_embeddings(model, df["clean"].tolist())

# Clustering
kmeans_labels, sil_score, km_model = run_kmeans(embeddings)
dbscan_labels = run_dbscan(embeddings)
df = attach_cluster_labels(df, kmeans_labels, dbscan_labels)

# Visualization
plot_tsne(embeddings, kmeans_labels)

# Summarization
summaries = summarize_clusters(df)
print("Cluster Summaries:",summaries)

#save visualization and summaries
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

plot_tsne(
    embeddings,
    kmeans_labels,
    save_path=os.path.join(OUTPUT_DIR, "cluster_plot.png"),
    title="KMeans Topic Clusters"
)

summary_file = os.path.join(OUTPUT_DIR, "cluster_summaries.json")
summaries = summarize_clusters(df, save_path=summary_file)
