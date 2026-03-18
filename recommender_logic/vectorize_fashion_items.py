import joblib
from scipy import sparse
import pandas as pd

vectorizer = joblib.load("tfidf_vectorizer.joblib")
X = sparse.load_npz("item_tfidf_matrix.npz")
index_df = pd.read_csv("item_index.csv")

vocab = vectorizer.get_feature_names_out()

image_id = 22896 
matches = index_df.index[index_df["image_id"] == image_id].tolist()

if not matches:
    raise ValueError(f"image_id {image_id} not found in item_index.csv")

row_idx = matches[0]
row_dense = X[row_idx].toarray()[0]

print("Image ID:", index_df.iloc[row_idx]["image_id"])

for token, value in zip(vocab, row_dense):
    # if value != 0:
    #     print(token, value)
    print(token, value)
