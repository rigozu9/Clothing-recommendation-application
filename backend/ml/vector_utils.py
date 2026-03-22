import numpy as np

def get_image_row_index(image_id, index_df):
    matches = index_df.index[index_df["image_id"] == image_id].tolist()

    if not matches:
        raise ValueError(f"image_id {image_id} not found")

    return matches[0]

def get_item_vector(image_id, index_df, X):
    row_idx = get_image_row_index(image_id, index_df)
    vector = X[row_idx].toarray()[0]
    return np.array(vector, dtype=float)