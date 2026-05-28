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

    image = cv2.resize(image, (640, 640))

    image = image.astype(np.float32) / 255.0

    image = image.transpose(2, 0, 1)

    image = np.expand_dims(image, axis=0)

    return image


def detect_hazard(image_path):

    session = get_session()

    input_image = preprocess(image_path)

    input_name = session.get_inputs()[0].name

    outputs = session.run(
        None,
        {input_name: input_image}
    )

    predictions = outputs[0]

    confidence_threshold = 0.4

    pothole_count = 0

    max_confidence = 0

    max_area = 0

    for detection in predictions[0]:

        if len(detection) < 5:
            continue

        confidence = float(
            np.max(detection[4:])
        )

        if confidence > confidence_threshold:

            pothole_count += 1

            x_center = float(detection[0])
            y_center = float(detection[1])

            width = float(detection[2])
            height = float(detection[3])

            area = width * height

            if confidence > max_confidence:

                max_confidence = confidence

                max_area = area

    if pothole_count == 0:

        return "no_hazard", 0, 0, 0

    if max_area < 500:

        return (
            "no_hazard",
            max_confidence,
            max_area,
            0
        )

    return (
        "pothole",
        max_confidence,
        max_area,
        pothole_count
    )