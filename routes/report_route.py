from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
from datetime import datetime
import tempfile
import pytz

from model.detect import detect_hazard
from services.severity_service import calculate_severity
from services.cost_service import estimate_repair_cost
from services.firebase_service import db

router = APIRouter()


@router.post("/report")
async def report_hazard(
    file: UploadFile = File(...),
    lat: float = Form(...),
    lon: float = Form(...),
    email: str = Form(...)
):
    print("EMAIL RECEIVED:", email)

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as temp:

        temp_path = temp.name

        shutil.copyfileobj(file.file, temp)

    hazard, confidence, area, pothole_count = detect_hazard(
        temp_path
    )

    if hazard == "no_hazard":

        os.remove(temp_path)

        return {
            "status": "no_hazard",
            "message": "No road hazard detected."
        }

    severity = calculate_severity(area)

    repair_cost = estimate_repair_cost(severity)

    india = pytz.timezone("Asia/Kolkata")

    current_time = datetime.now(india)

    data = {
        "hazard_type": hazard,
        "pothole_count": pothole_count,
        "severity": severity,
        "repair_cost": repair_cost,
        "latitude": lat,
        "longitude": lon,

        # KEEP THIS
        "timestamp": current_time.isoformat()
    }

    db.collection("hazards").add(data)

    print("REPORT SUBMITTED BY:", email)

    user_query = db.collection("users").where(
        "email",
        "==",
        email
    ).stream()

    found = False

    for user in user_query:

        found = True

        user_data = user.to_dict()

        print("USER FOUND:", user_data)

        current_points = user_data.get("points", 0)

        db.collection("users").document(user.id).update({
            "points": current_points + 10
        })

        print("POINTS UPDATED")

    if not found:
        print("USER NOT FOUND")

    os.remove(temp_path)

    return {
        "status": "success",
        "points_added": 10,
        "data": data
    }