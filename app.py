from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import report_route
from routes import hazards_to_map
from routes import auth_route
from routes import leaderboard_route
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# CORS configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(report_route.router)
app.include_router(hazards_to_map.router)
app.include_router(auth_route.router)
app.include_router(leaderboard_route.router)

@app.get("/")
def home():
    return {"message": "RoadSense API Running"}