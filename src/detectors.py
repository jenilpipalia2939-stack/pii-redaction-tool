import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9-]+"
    r"(?:\r?\n[A-Za-z0-9-]+)*"
    r"(?:\.[A-Za-z0-9-]+)+\b"
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