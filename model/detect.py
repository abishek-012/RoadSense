import cv2
import numpy as np
import onnxruntime as ort

session = None


def get_session():

    global session

    if session is None:

        session = ort.InferenceSession(
            "model/pothole.onnx",
            providers=["CPUExecutionProvider"]
        )

    return session


def preprocess(image_path):

    image = cv2.imread(image_path)

    original = image.copy()

    image = cv2.resize(image, (640, 640))

    image = image / 255.0

    image = image.transpose(2, 0, 1)

    image = np.expand_dims(image, axis=0).astype(np.float32)

    return image, original


def detect_hazard(image_path):

    session = get_session()

    input_image, original = preprocess(image_path)

    input_name = session.get_inputs()[0].name

    outputs = session.run(
        None,
        {input_name: input_image}
    )

    predictions = outputs[0]

    confidence_threshold = 0.6

    pothole_count = 0

    max_confidence = 0

    max_area = 0

    for detection in predictions[0]:

        confidence = float(detection[4])

        if confidence > confidence_threshold:

            pothole_count += 1

            x_center, y_center, width, height = detection[:4]

            area = width * height

            if confidence > max_confidence:

                max_confidence = confidence

                max_area = area

    if pothole_count == 0:

        return "no_hazard", 0, 0, 0

    if max_area < 5000:

        return "no_hazard", max_confidence, max_area, 0

    return (
        "pothole",
        max_confidence,
        max_area,
        pothole_count
    )