import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9-]+"
    r"(?:\r?\n[A-Za-z0-9-]+)*"
    r"(?:\.[A-Za-z0-9-]+)+\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:"
    r"\+\s*91[\s-]*"
    r"(?:\d[\s-]*){10}"
    r"|"
    r"\b[6-9]\d{9}\b"
    r")"
    r"(?!\d)"
)

def detect_emails(text):
    matches = []

    for match in EMAIL_PATTERN.finditer(text):
        raw_value = match.group(0)

        normalized_value = re.sub(r"\r?\n", "", raw_value)

        matches.append({
            "type": "EMAIL",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches

def detect_phone_numbers(text):
    matches = []

    for match in PHONE_PATTERN.finditer(text):
        raw_value = match.group(0)

        normalized_value = re.sub(r"[\s-]", "", raw_value)

        matches.append({
            "type": "PHONE",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches