import pandas as pd
from sqlalchemy import create_engine

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
print(df.head())
print(df.shape)