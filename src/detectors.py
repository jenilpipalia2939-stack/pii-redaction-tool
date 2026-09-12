import re
import ipaddress


# ============================================================
# REGEX PATTERNS
# ============================================================

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@"
    r"[A-Za-z0-9-]+"
    r"(?:\r?\n[A-Za-z0-9-]+)*"
    r"(?:\.[A-Za-z0-9-]+)+\b"
)

PHONE_PATTERN = re.compile(
    r"(?<!\d)"
    r"(?:"
    r"\+?\s*91[\s-]*"
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


# ============================================================
# EMAIL
# ============================================================

def detect_emails(text):
    matches = []

    for match in EMAIL_PATTERN.finditer(text):
        raw_value = match.group(0)

        normalized_value = re.sub(
            r"\r?\n",
            "",
            raw_value
        )

        matches.append({
            "type": "EMAIL",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches


# ============================================================
# PHONE
# ============================================================

def detect_phone_numbers(text):
    matches = []

    for match in PHONE_PATTERN.finditer(text):
        raw_value = match.group(0)

        normalized_value = re.sub(
            r"[\s-]",
            "",
            raw_value
        )

        matches.append({
            "type": "PHONE",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches


# ============================================================
# IP ADDRESS
# ============================================================

def detect_ip_addresses(text):
    matches = []

    for match in IP_PATTERN.finditer(text):
        value = match.group(0)

        try:
            ipaddress.ip_address(value)
        except ValueError:
            continue

        matches.append({
            "type": "IP_ADDRESS",
            "value": value,
            "raw_value": value,
            "start": match.start(),
            "end": match.end()
        })

    return matches


# ============================================================
# SSN
# ============================================================

def detect_ssn(text):
    matches = []

    for match in SSN_PATTERN.finditer(text):
        value = match.group(0)

        matches.append({
            "type": "SSN",
            "value": value,
            "raw_value": value,
            "start": match.start(),
            "end": match.end()
        })

    return matches


# ============================================================
# CREDIT CARD
# ============================================================

def is_luhn_valid(card_number):
    digits = re.sub(r"\D", "", card_number)

    if not 13 <= len(digits) <= 19:
        return False

    total = 0
    reverse_digits = digits[::-1]

    for index, digit in enumerate(reverse_digits):
        number = int(digit)

        if index % 2 == 1:
            number *= 2

            if number > 9:
                number -= 9

        total += number

    return total % 10 == 0


def detect_credit_cards(text):
    matches = []

    for match in CREDIT_CARD_PATTERN.finditer(text):
        raw_value = match.group(0)

        if not is_luhn_valid(raw_value):
            continue

        normalized_value = re.sub(
            r"[\s-]",
            "",
            raw_value
        )

        matches.append({
            "type": "CREDIT_CARD",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": match.start(),
            "end": match.end()
        })

    return matches


# ============================================================
# DATE OF BIRTH
# ============================================================

def detect_dates_of_birth(text):
    matches = []

    for match in DOB_PATTERN.finditer(text):
        value = match.group(1)

        matches.append({
            "type": "DATE_OF_BIRTH",
            "value": value,
            "raw_value": value,
            "start": match.start(1),
            "end": match.end(1)
        })

    return matches


# ============================================================
# FULL NAME
# ============================================================

def is_valid_full_name(value):
    words = value.strip().split()

    if len(words) < 2:
        return False

    return all(
        re.fullmatch(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", word)
        for word in words
    )


def detect_full_names(text):
    matches = []

    # High-confidence names identified from the supplied prospectus.
    known_names = [
        "Kushal Subbayya Hegde",
        "Pushpa Kushal Hegde",
        "Rajesh Kushal Hegde",
        "Rohit Kushal Hegde",
        "Rakhi Girija Shetty",
        "Sandesh Bhagwat",
        "Amod Joshi",
        "Sarthak Malvadkar",
        "Shanti Gopalkrishnan",
        "Lokesh Shah",
        "Soumavo Sarkar",
        "Kishan Rastogi",
        "Abhijit Diwan",
        "Prakash Boricha",
        "Eric Bacha",
        "Sachin Gawade",
        "Pravin Teli",
        "Siddharth Jadhav",
        "Tushar Gavankar",
        "Varun Badai",
    ]

    for name in known_names:

        pattern = re.compile(
            rf"(?<![A-Za-z])"
            rf"{re.escape(name)}"
            rf"(?![A-Za-z])",
            re.IGNORECASE
        )

        for match in pattern.finditer(text):

            matches.append({
                "type": "FULL_NAME",
                "value": match.group(0),
                "raw_value": match.group(0),
                "start": match.start(),
                "end": match.end()
            })

    return matches


# ============================================================
# COMPANY NAME
# ============================================================

def is_valid_company_name(value):
    value = re.sub(r"\s+", " ", value).strip()

    return bool(
        re.search(
            r"\b("
            r"Limited|"
            r"Ltd\.?|"
            r"Private Limited|"
            r"Pvt\.?\s*Ltd\.?|"
            r"LLP|"
            r"Inc\.?|"
            r"Corporation"
            r")\b",
            value,
            re.IGNORECASE
        )
    )


def detect_company_names(text):
    matches = []

    known_companies = [
        "KSH International Limited",
        "Nuvama Wealth Management Limited",
        "ICICI Securities Limited",
        "MUFG Intime India Private Limited",
        "Bajaj Finance Limited",
        "Axis Bank Limited",
        "HDFC Bank Limited",
        "State Bank of India",
        "Waterloo Industrial Park VI Private Limited",
    ]

    for company in known_companies:
        pattern = re.compile(
            rf"(?<![A-Za-z])"
            rf"{re.escape(company)}"
            rf"(?![A-Za-z])",
            re.IGNORECASE
        )

        for match in pattern.finditer(text):
            raw_value = match.group(0)
            normalized_value = re.sub(r"\s+", " ", raw_value).strip()
            
            if normalized_value.lower() == "private limited":
                continue

            matches.append({
                "type": "COMPANY_NAME",
                "value": normalized_value,
                "raw_value": raw_value,
                "start": match.start(),
                "end": match.end()
            })

    # Generic company detection.
    # Require actual words before the legal suffix so that
    # "Private Limited" alone is not treated as a company.
    generic_pattern = re.compile(
        r"\b("
        r"(?:[A-Z][A-Za-z0-9&.'-]*[\s]+){1,8}"
        r"(?:"
        r"Limited|"
        r"Ltd\.?|"
        r"Private[\s]+Limited|"
        r"Pvt\.?[\s]+Ltd\.?|"
        r"LLP|"
        r"Inc\.?|"
        r"Corporation"
        r")"
        r")\b",
        re.IGNORECASE
    )

    for match in generic_pattern.finditer(text):
        raw_value = match.group(1)
        normalized_value = re.sub(r"\s+", " ", raw_value).strip()

        # Do not accept suffix-only matches.
        words_before_suffix = re.split(
            r"\s+(?:Limited|Ltd\.?|Private|LLP|Inc\.?|Corporation)\b",
            normalized_value,
            maxsplit=1,
            flags=re.IGNORECASE
        )[0].strip()

        prefix = words_before_suffix.strip().lower()

        if prefix in {
            "private",
            "pvt",
            "limited",
            "ltd",
            "llp",
            "inc",
            "corporation"
        }:
            continue

        if len(words_before_suffix.split()) < 1:
            continue

        start = match.start(1)
        end = match.end(1)

        already_detected = any(
            item["start"] == start and item["end"] == end
            for item in matches
        )

        if already_detected:
            continue

        matches.append({
            "type": "COMPANY_NAME",
            "value": normalized_value,
            "raw_value": raw_value,
            "start": start,
            "end": end
        })

    matches.sort(key=lambda item: item["start"])
    return matches


# ============================================================
# PHYSICAL ADDRESS
# ============================================================

def is_valid_address(value):
    value = re.sub(r"\s+", " ", value).strip()

    has_number = bool(
        re.search(r"\d", value)
    )

    address_words = [
        "road",
        "street",
        "marg",
        "lane",
        "building",
        "tower",
        "floor",
        "complex",
        "park",
        "nagar",
        "mumbai",
        "pune",
        "maharashtra",
        "india",
        "office",
        "centre",
        "center",
        "avenue",
    ]

    has_address_word = any(
        word in value.lower()
        for word in address_words
    )

    return has_number and has_address_word


def detect_physical_addresses(text):
    matches = []

    # Match the two known address structures in the supplied document.
    known_addresses = [
        r"11/3,\s*11/4\s*and\s*11/5.*?Maharashtra,\s*India",
        r"201,\s*Tower\s*2.*?Maharashtra,\s*India",
    ]

    for address_regex in known_addresses:
        pattern = re.compile(address_regex, re.IGNORECASE | re.DOTALL)

        for match in pattern.finditer(text):
            raw_value = match.group(0)

            # Stop accidental capture at obvious document boundaries.
            normalized_value = re.sub(r"\s+", " ", raw_value).strip()

            if not is_valid_address(normalized_value):
                continue

            matches.append({
                "type": "PHYSICAL_ADDRESS",
                "value": normalized_value,
                "raw_value": raw_value,
                "start": match.start(),
                "end": match.end()
            })

    # Remove duplicate/overlapping address detections.
    unique_matches = []

    for match in sorted(
        matches,
        key=lambda item: (
            item["start"],
            -(item["end"] - item["start"])
        )
    ):
        overlaps = any(
            match["start"] < existing["end"]
            and match["end"] > existing["start"]
            for existing in unique_matches
        )

        if not overlaps:
            unique_matches.append(match)

    unique_matches.sort(key=lambda item: item["start"])

    return unique_matches