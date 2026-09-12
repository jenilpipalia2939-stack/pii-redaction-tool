from detectors import detect_phone_numbers


def test_detect_indian_phone_number():
    text = "Contact us at +91 22 4009 4400"

    phones = detect_phone_numbers(text)

    assert len(phones) == 1
    assert phones[0]["value"] == "+912240094400"


def test_detect_phone_number_with_newlines():
    text = "Telephone: +91\n22\n40094400"

    phones = detect_phone_numbers(text)

    assert len(phones) == 1
    assert phones[0]["value"] == "+912240094400"


def test_detect_hyphenated_phone_number():
    text = "Telephone: +91-20-26234000"

    phones = detect_phone_numbers(text)

    assert len(phones) == 1
    assert phones[0]["value"] == "+912026234000"


def test_ignore_normal_number():
    text = "The amount is 40094400"

    phones = detect_phone_numbers(text)

    assert len(phones) == 0