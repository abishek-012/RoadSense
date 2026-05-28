from fastapi import APIRouter
from services.firebase_service import db
from google.cloud.firestore_v1 import Query

router = APIRouter()

@router.get("/hazards")
def hazards_to_map():

    hazards = []

    docs = db.collection("hazards") \
        .order_by("timestamp", direction=Query.DESCENDING) \
        .stream()

    for doc in docs:

        hazard = doc.to_dict()

        hazards.append(hazard)

    return hazards