from ultralytics import YOLO

model = YOLO("model/pothole.pt")

def detect_hazard(image_path):

    results = model(image_path)

    boxes = results[0].boxes

    # No detection
    if boxes is None or len(boxes) == 0:
        return "no_hazard", 0, 0, 0

    pothole_count = len(boxes)

    confidence = float(boxes.conf[0])

    box = boxes.xyxy[0]

    x1 = float(box[0])
    y1 = float(box[1])
    x2 = float(box[2])
    y2 = float(box[3])

    width = x2 - x1
    height = y2 - y1

    area = width * height

    if confidence < 0.6 or area < 5000:
        return "no_hazard", confidence, area, 0

    return "pothole", confidence, area, pothole_count