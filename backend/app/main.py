from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.models
from app.routes import users, style_vectors, images, plotdata

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
app.include_router(images.router, prefix="/images", tags=["images"])
app.include_router(plotdata.router, prefix="/plotdata", tags=["plotdata"])


@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/pong")
def pong():
    return {"message": "Ping pongiong!"}