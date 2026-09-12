import re
import ipaddress

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

IP_PATTERN = re.compile(
    r"(?<![\w.])"
    r"(?:\d{1,3}\.){3}\d{1,3}"
    r"(?![\w.])"
)

SSN_PATTERN = re.compile(
    r"(?<![\d-])"
    r"\d{3}-\d{2}-\d{4}"
    r"(?![\d-])"
)

CREDIT_CARD_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:\d[ -]?){13,19}"
    r"(?!\d)"
)

DOB_PATTERN = re.compile(
    r"(?i)"
    r"(?:date\s+of\s+birth|dob|birth\s+date)"
    r"\s*[:\-]?\s*"
    r"("
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}"
    r"|"
    r"\d{1,2}\s+[A-Za-z]+\s+\d{4}"
    r"|"
    r"[A-Za-z]+\s+\d{1,2},\s+\d{4}"
    r")"
)

NAME_PATTERN = re.compile(
    r"(?i)"
    r"(?:contact\s+person|contact\s+persons?)"
    r"\s*[:\-]\s*"
    r"([^;\r\n]+)"
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

def detect_ip_addresses(text):
    matches = []

    for match in IP_PATTERN.finditer(text):
        raw_value = match.group(0)

        try:
            ipaddress.ip_address(raw_value)
        except ValueError:
            continue

        matches.append({
            "type": "IP_ADDRESS",
            "value": raw_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches

def detect_ssn(text):
    matches = []

    for match in SSN_PATTERN.finditer(text):
        raw_value = match.group(0)

        matches.append({
            "type": "SSN",
            "value": raw_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches

def is_luhn_valid(number):
    digits = [int(digit) for digit in number]

    checksum = 0
    parity = len(digits) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


def detect_credit_cards(text):
    matches = []

    for match in CREDIT_CARD_PATTERN.finditer(text):
        raw_value = match.group(0)

        normalized_value = re.sub(r"[ -]", "", raw_value)

        if not 13 <= len(normalized_value) <= 19:
            continue

        if not is_luhn_valid(normalized_value):
            continue

        matches.append({
            "type": "CREDIT_CARD",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches

def detect_dates_of_birth(text):
    matches = []

    for match in DOB_PATTERN.finditer(text):
        raw_value = match.group(1)

        matches.append({
            "type": "DATE_OF_BIRTH",
            "value": raw_value,
            "raw_value": raw_value,
            "start": match.start(1),
            "end": match.end(1)
        })

    return matches


def is_valid_full_name(name):
    words = name.strip().split()

    if not 2 <= len(words) <= 5:
        return False

    blocked_words = {
        "sebi",
        "registration",
        "number",
        "no",
        "website",
        "email",
        "telephone",
        "contact",
        "person",
        "company",
        "limited"
    }

    if any(word.lower() in blocked_words for word in words):
        return False

    return all(
        re.fullmatch(r"[A-Za-z]+", word)
        for word in words
    )

def is_valid_full_name(name):
    words = name.strip().split()

    if not 2 <= len(words) <= 5:
        return False

    blocked_words = {
        "sebi",
        "registration",
        "number",
        "no",
        "website",
        "email",
        "telephone",
        "contact",
        "person",
        "company",
        "limited"
    }

    if any(word.lower() in blocked_words for word in words):
        return False

    return all(
        re.fullmatch(r"[A-Za-z]+", word)
        for word in words
    )

def detect_full_names(text):
    matches = []

    for match in NAME_PATTERN.finditer(text):
        raw_value = match.group(1).strip()

        names = re.split(r"\s*/\s*", raw_value)

        current_position = match.start(1)

        for name in names:
            name = name.strip()

            if not is_valid_full_name(name):
                continue

            start = text.find(name, current_position, match.end(1))

            if start == -1:
                continue

            matches.append({
                "type": "FULL_NAME",
                "value": name,
                "raw_value": name,
                "start": start,
                "end": start + len(name)
            })

            current_position = start + len(name)

    return matches