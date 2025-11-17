from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_score
import pandas as pd

def run_kmeans(embeddings,k=5):
    kmeans = KMeans(n_clusters=k, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    sil = silhouette_score(embeddings, labels)
    return labels, sil, kmeans

def run_dbscan(embeddings, eps=0.2, min_samples=5):
    db = DBSCAN(eps=eps, min_samples=min_samples)
    labels = db.fit_predict(embeddings)
    return labels

def attach_cluster_labels(df, kmeans_labels, dbscan_labels):
    df["kmeans_cluster"] = kmeans_labels
    df["dbscan_cluster"] = dbscan_labels
    df["is_outlier"] = df["dbscan_cluster"].apply(lambda x: 1 if x == -1 else 0)
    return df