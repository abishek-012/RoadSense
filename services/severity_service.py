def calculate_severity(box_area):

    if box_area < 5000:
        return "low"

    elif box_area < 20000:
        return "medium"

    else:
        return "high"