
from src.faker import generate_fake_value


def remove_overlapping_detections(detections):
    """
    Remove overlapping detections.

    If two detections overlap, keep the larger detection.
    This prevents one replacement from corrupting another.
    """

    sorted_detections = sorted(
        detections,
        key=lambda item: (
            item["start"],
            -(item["end"] - item["start"])
        )
    )

    accepted = []

    for detection in sorted_detections:
        overlaps = False

        for existing in accepted:
            if (
                detection["start"] < existing["end"]
                and detection["end"] > existing["start"]
            ):
                overlaps = True
                break

        if not overlaps:
            accepted.append(detection)

    return accepted


def redact_text(text, detections):
    """
    Replace detected PII with fake values.

    The same original PII value always receives
    the same fake replacement.
    """

    detections = remove_overlapping_detections(detections)

    replacement_map = {}

    # Replace from the end of the document toward the beginning.
    detections = sorted(
        detections,
        key=lambda item: item["start"],
        reverse=True
    )

    redacted_text = text

    for detection in detections:
        original_value = detection["value"]
        pii_type = detection["type"]

        if pii_type == "FULL_NAME":
            map_key = original_value.lower().strip()
        else:
            map_key = original_value

        if map_key not in replacement_map:
            replacement_map[map_key] = generate_fake_value(pii_type)

        fake_value = replacement_map[map_key]
        start = detection["start"]
        end = detection["end"]

        redacted_text = (
            redacted_text[:start]
            + fake_value
            + redacted_text[end:]
        )

    return redacted_text, replacement_map

