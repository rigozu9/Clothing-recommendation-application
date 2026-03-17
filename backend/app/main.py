from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, style_vectors

app = FastAPI(title="Clothing Recommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(style_vectors.router, prefix="/style-vectors", tags=["style-vectors"])


@app.get("/")
def root():
    return {"message": "API is running"}