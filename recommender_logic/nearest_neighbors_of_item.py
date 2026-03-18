import joblib
from scipy import sparse
import pandas as pd
from sklearn.neighbors import NearestNeighbors

def get_similar_items(image_id, index_df, X, nn_model, top_k=5):
    matches = index_df.index[index_df["image_id"] == image_id].tolist()

    if not matches:
        raise ValueError(f"image_id {image_id} not found")

    query_idx = matches[0]

    distances, indices = nn_model.kneighbors(X[query_idx], n_neighbors=top_k + 1)

    neighbor_rows = indices[0]
    neighbor_distances = distances[0]

    result = index_df.iloc[neighbor_rows].copy()
    result["distance"] = neighbor_distances
    result["similarity"] = 1 - result["distance"]

    result = result[result["image_id"] != image_id].head(top_k)

    return result

image_id = 268916
index_df = pd.read_csv("item_index.csv")
X = sparse.load_npz("item_tfidf_matrix.npz")
nn_model = NearestNeighbors(metric="cosine", algorithm="brute")
nn_model.fit(X)

vectorizer = joblib.load("tfidf_vectorizer.joblib")

result = get_similar_items(image_id, index_df, X, nn_model, top_k=10)
print(result)

ids = result["image_id"].tolist()
ids.insert(0, image_id)  # include query item

sql = f"""
SELECT image_id, url
FROM raw.imat_images
WHERE image_id IN ({",".join(map(str, ids))});
"""

print(sql)
