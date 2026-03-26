from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, style_vectors, images, plotdata, user_likes, recommendations

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
app.include_router(user_likes.router, prefix="/users", tags=["users"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
def root():
    return {"message": "API is running"}

@app.get("/pong")
def pong():
    return {"message": "Ping pongiong!"}