import joblib
from scipy import sparse
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

def get_image_row_index(image_id, index_df):
    matches = index_df.index[index_df["image_id"] == image_id].tolist()

    if not matches:
        raise ValueError(f"image_id {image_id} not found")

    return matches[0]


def get_similar_items_from_row(query_vector, index_df, X, nn_model, top_k=5, exclude_image_ids=None):
    if exclude_image_ids is None:
        exclude_image_ids = []

    distances, indices = nn_model.kneighbors(query_vector, n_neighbors=top_k + len(exclude_image_ids) + 10)

    neighbor_rows = indices[0]
    neighbor_distances = distances[0]

    result = index_df.iloc[neighbor_rows].copy()
    result["distance"] = neighbor_distances
    result["similarity"] = 1 - result["distance"]

    if exclude_image_ids:
        result = result[~result["image_id"].isin(exclude_image_ids)]

    result = result.head(top_k).reset_index(drop=True)
    return result


def get_similar_items(image_id, index_df, X, nn_model, top_k=5):
    query_idx = get_image_row_index(image_id, index_df)
    query_vector = X[query_idx]

    result = get_similar_items_from_row(
        query_vector=query_vector,
        index_df=index_df,
        X=X,
        nn_model=nn_model,
        top_k=top_k,
        exclude_image_ids=[image_id]
    )

    return result


def build_fake_user_vector_from_neighbors(seed_image_id, index_df, X, nn_model, neighbor_k=10):
    # 1. get neighbors of the seed item
    neighbors = get_similar_items(seed_image_id, index_df, X, nn_model, top_k=neighbor_k)

    # 2. get their row indices
    neighbor_image_ids = neighbors["image_id"].tolist()
    neighbor_rows = index_df.index[index_df["image_id"].isin(neighbor_image_ids)].tolist()

    # 3. average their tf-idf vectors
    neighbor_matrix = X[neighbor_rows]
    mean_vector_dense = neighbor_matrix.mean(axis=0)

    # convert numpy matrix -> csr sparse matrix so kneighbors works nicely
    fake_user_vector = sparse.csr_matrix(mean_vector_dense)

    return fake_user_vector, neighbors


# -------------------------
# LOAD DATA
# -------------------------
image_id = 551116

index_df = pd.read_csv("item_index.csv")
X = sparse.load_npz("item_tfidf_matrix.npz")
vectorizer = joblib.load("tfidf_vectorizer.joblib")

nn_model = NearestNeighbors(metric="cosine", algorithm="brute")
nn_model.fit(X)

# -------------------------
# STEP 1: build fake user vector
# -------------------------
fake_user_vector, seed_neighbors = build_fake_user_vector_from_neighbors(
    seed_image_id=image_id,
    index_df=index_df,
    X=X,
    nn_model=nn_model,
    neighbor_k=10
)

print("Seed item's nearest neighbors used to build fake user vector:")
print(seed_neighbors)

# -------------------------
# STEP 2: get recommendations from fake user vector
# -------------------------
exclude_ids = [image_id] + seed_neighbors["image_id"].tolist()

user_recommendations = get_similar_items_from_row(
    query_vector=fake_user_vector,
    index_df=index_df,
    X=X,
    nn_model=nn_model,
    top_k=10,
    exclude_image_ids=exclude_ids
)

print("\nRecommendations from fake user vector:")
print(user_recommendations)

# -------------------------
# STEP 3: inspect top features in fake user vector
# -------------------------
feature_names = vectorizer.get_feature_names_out()
fake_user_dense = fake_user_vector.toarray()[0]

top_feature_indices = np.argsort(fake_user_dense)[::-1][:20]

print("\nTop features in fake user vector:")
for idx in top_feature_indices:
    if fake_user_dense[idx] > 0:
        print(f"{feature_names[idx]}: {fake_user_dense[idx]:.4f}")

# -------------------------
# STEP 4: SQL for image urls
# -------------------------
recommended_ids = user_recommendations["image_id"].tolist()

sql = f"""
SELECT image_id, url
FROM raw.imat_images
WHERE image_id IN ({",".join(map(str, recommended_ids))});
"""

print("\nSQL to fetch recommended image URLs:")
print(sql)