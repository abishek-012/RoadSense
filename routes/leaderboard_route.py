from fastapi import APIRouter
from services.firebase_service import db

router = APIRouter()

@router.get("/leaderboard")
def get_leaderboard():

    users = db.collection("users").stream()

    leaderboard = []

    for user in users:

        data = user.to_dict()

        if data.get("role") == "user":

            leaderboard.append({
                "name": data["name"],
                "points": data.get("points",0)
            })

    leaderboard.sort(key=lambda x: x["points"], reverse=True)

    return leaderboard