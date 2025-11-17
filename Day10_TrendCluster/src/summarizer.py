import json

def summarize_clusters(df, cluster_col="kmeans_cluster", text_col="post", save_path=None):
    summary = {}

    for c in df[cluster_col].unique():
        posts = df[df[cluster_col] == c][text_col].tolist()
        summary[str(int(c))] = posts[:10]  # convert key to str

    if save_path:
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=4, ensure_ascii=False)

        print(f"Summary saved to {save_path}")

    return summary
