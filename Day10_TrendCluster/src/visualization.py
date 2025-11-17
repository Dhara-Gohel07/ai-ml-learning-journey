import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import os

def plot_tsne(embeddings, labels, save_path=None, title="Cluster Visualization"):
    tsne = TSNE(n_components=2, perplexity=15, random_state=42)
    tsne_result = tsne.fit_transform(embeddings)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(tsne_result[:, 0], tsne_result[:, 1], c=labels, cmap="tab10")
    plt.legend(*scatter.legend_elements(), title="Clusters")
    plt.title(title)

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"Plot saved to {save_path}")

    plt.close()   
