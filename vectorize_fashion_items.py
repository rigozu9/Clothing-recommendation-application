import joblib
from scipy import sparse
import pandas as pd

vectorizer = joblib.load("tfidf_vectorizer.joblib")
X = sparse.load_npz("item_tfidf_matrix.npz")
index_df = pd.read_csv("item_index.csv")

vocab = vectorizer.get_feature_names_out()

row_idx = 0
row_dense = X[row_idx].toarray()[0]

vocab = vectorizer.get_feature_names_out()

print("Image ID:", index_df.iloc[row_idx]["image_id"])

for token, value in zip(vocab, row_dense):
    print(token, value)