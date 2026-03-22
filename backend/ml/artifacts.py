from pathlib import Path
import pandas as pd
from scipy import sparse


BASE_DIR = Path(__file__).resolve().parents[3]
RECOMMENDER_DIR = BASE_DIR / "recommender_logic"

INDEX_PATH = RECOMMENDER_DIR / "item_index.csv"
MATRIX_PATH = RECOMMENDER_DIR / "item_tfidf_matrix.npz"


index_df = pd.read_csv(INDEX_PATH)
X = sparse.load_npz(MATRIX_PATH)