from detectors import detect_phone_numbers
from detectors import detect_ip_addresses
from detectors import detect_ssn


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


def test_detect_valid_ip_address():
    text = "Client IP address: 192.168.1.100"

    ips = detect_ip_addresses(text)

    assert len(ips) == 1
    assert ips[0]["value"] == "192.168.1.100"


def test_reject_invalid_ip_address():
    text = "Invalid IP address: 999.999.999.999"

    ips = detect_ip_addresses(text)

    assert len(ips) == 0


def test_ignore_non_ip_number():
    text = "The amount is 192.168.1000"

    ips = detect_ip_addresses(text)

    assert len(ips) == 0
def test_detect_ssn():
    text = "SSN: 123-45-6789"

    ssns = detect_ssn(text)

    assert len(ssns) == 1
    assert ssns[0]["value"] == "123-45-6789"


def test_ignore_number_without_ssn_format():
    text = "Reference number: 123456789"

    ssns = detect_ssn(text)

    assert len(ssns) == 0


def test_ignore_invalid_ssn_length():
    text = "Invalid SSN: 123-456-789"

    ssns = detect_ssn(text)

    assert len(ssns) == 0