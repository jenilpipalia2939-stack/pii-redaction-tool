from detectors import detect_phone_numbers
from detectors import detect_ip_addresses
from detectors import detect_ssn
from detectors import detect_credit_cards
from detectors import detect_dates_of_birth
from detectors import detect_full_names


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

def test_detect_credit_card():
    text = "Card number: 4111 1111 1111 1111"

    cards = detect_credit_cards(text)

    assert len(cards) == 1
    assert cards[0]["value"] == "4111111111111111"


def test_detect_hyphenated_credit_card():
    text = "Card number: 4111-1111-1111-1111"

    cards = detect_credit_cards(text)

    assert len(cards) == 1
    assert cards[0]["value"] == "4111111111111111"


def test_reject_invalid_credit_card():
    text = "Card number: 4111 1111 1111 1112"

    cards = detect_credit_cards(text)

    assert len(cards) == 0


def test_ignore_normal_long_number():
    text = "Reference number: 1234567890123456"

    cards = detect_credit_cards(text)

    assert len(cards) == 0

def test_detect_dob_slash_format():
    text = "Date of Birth: 15/08/1998"

    result = detect_dates_of_birth(text)

    assert len(result) == 1
    assert result[0]["type"] == "DATE_OF_BIRTH"
    assert result[0]["value"] == "15/08/1998"


def test_detect_dob_hyphen_format():
    text = "DOB: 15-08-1998"

    result = detect_dates_of_birth(text)

    assert len(result) == 1
    assert result[0]["value"] == "15-08-1998"


def test_detect_dob_text_format():
    text = "Birth Date: 15 August 1998"

    result = detect_dates_of_birth(text)

    assert len(result) == 1
    assert result[0]["value"] == "15 August 1998"


def test_do_not_detect_normal_date():
    text = "Prospectus dated 10/12/2025"

    result = detect_dates_of_birth(text)

    assert len(result) == 0

def test_detect_single_full_name():
    text = "Contact Person: Sarthak Malvadkar"

    result = detect_full_names(text)

    assert len(result) == 1
    assert result[0]["type"] == "FULL_NAME"
    assert result[0]["value"] == "Sarthak Malvadkar"


def test_detect_multiple_contact_persons():
    text = "Contact Person: Lokesh Shah/ Soumavo Sarkar"

    result = detect_full_names(text)

    assert len(result) == 2
    assert result[0]["value"] == "Lokesh Shah"
    assert result[1]["value"] == "Soumavo Sarkar"


def test_detect_five_contact_persons():
    text = (
        "Contact Person: Eric Bacha/ Sachin Gawade/ "
        "Pravin Teli/ Siddharth Jadhav/ Tushar Gavankar"
    )

    result = detect_full_names(text)

    assert len(result) == 5
    assert result[0]["value"] == "Eric Bacha"
    assert result[4]["value"] == "Tushar Gavankar"


def test_do_not_detect_random_capitalized_words():
    text = "KSH International Limited is located in Mumbai."

    result = detect_full_names(text)

    assert len(result) == 0