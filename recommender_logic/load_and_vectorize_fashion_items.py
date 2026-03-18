import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
from scipy import sparse

engine = create_engine("postgresql+psycopg2://postgres:postgres@localhost:5434/fashion")

query = """
select
    split,
    image_id,
    tokens
from analytics.int_imat_image_token_lists
order by split, image_id
"""

df = pd.read_sql(query, engine)
# print(df.head())
# print(df.shape)

# For every row, if the tokens column contains a list, 
# join the tokens together into a space-separated string. Otherwise return an empty string.
df["token_text"] = df["tokens"].apply(lambda x: " ".join(x) if isinstance(x, list) else "")
# print(df[["image_id", "token_text"]].head())

vectorizer = TfidfVectorizer(
    tokenizer=str.split,
    preprocessor=None,
    token_pattern=None,
    lowercase=False
)

X = vectorizer.fit_transform(df["token_text"])

# print(X.shape)
# print(len(vectorizer.get_feature_names_out()))
# print(vectorizer.get_feature_names_out()[:20])
# print(vectorizer.get_feature_names_out()[50:70])

# vocab = vectorizer.get_feature_names_out()

# row_idx = 100
# row = X[row_idx]
# nonzero_indices = row.nonzero()[1]

# for idx in nonzero_indices:
#     print(vocab[idx], row[0, idx])


joblib.dump(vectorizer, "tfidf_vectorizer.joblib")
sparse.save_npz("item_tfidf_matrix.npz", X)

df[["split", "image_id"]].to_csv("item_index.csv", index=False)