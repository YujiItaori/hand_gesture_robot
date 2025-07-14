def detect_gesture(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    thumb_ip = landmarks[3]
    index_dip = landmarks[6]
    middle_dip = landmarks[10]
    ring_dip = landmarks[14]
    pinky_dip = landmarks[18]

    if (
        thumb_tip.y < thumb_ip.y and
        index_tip.y > index_dip.y and
        middle_tip.y > middle_dip.y and
        ring_tip.y > ring_dip.y and
        pinky_tip.y > pinky_dip.y
    ):
        return "Thumbs Up", "Pick Object"

    if (
        thumb_tip.y > thumb_ip.y and
        index_tip.y > index_dip.y and
        middle_tip.y > middle_dip.y and
        ring_tip.y > ring_dip.y and
        pinky_tip.y > pinky_dip.y
    ):
        return "Thumbs Down", "Release Object"

    if (
        index_tip.y < index_dip.y and
        middle_tip.y < middle_dip.y and
        ring_tip.y < ring_dip.y and
        pinky_tip.y < pinky_dip.y
    ):
        return "Open Palm", "Move Forward"

    if (
        index_tip.y > index_dip.y and
        middle_tip.y > middle_dip.y and
        ring_tip.y > ring_dip.y and
        pinky_tip.y > pinky_dip.y and
        thumb_tip.y > thumb_ip.y
    ):
        return "Fist", "Stop"

    return "Unknown", "No Action"
