import random


FIRST_NAMES = [
    "Aarav",
    "Vivaan",
    "Aditya",
    "Arjun",
    "Rohan",
    "Karan",
    "Rahul",
    "Vikram",
    "Neeraj",
    "Sahil",
]

LAST_NAMES = [
    "Mehta",
    "Shah",
    "Patel",
    "Verma",
    "Kapoor",
    "Malhotra",
    "Joshi",
    "Desai",
    "Rao",
    "Singh",
]

DOMAINS = [
    "example.com",
    "example.org",
]


def generate_fake_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def generate_fake_email():
    name = generate_fake_name().lower().replace(" ", ".")
    domain = random.choice(DOMAINS)

    return f"{name}@{domain}"


def generate_fake_phone():
    return "+91 90000 " + str(random.randint(10000, 99999))


def generate_fake_address():
    house_number = random.randint(10, 999)

    return (
        f"{house_number}, Example Business Park, "
        f"MG Road, Pune – 411 001, Maharashtra, India"
    )


def generate_fake_company():
    companies = [
        "Apex Technologies Private Limited",
        "Bluewave Solutions Limited",
        "Vertex Industrial Systems Private Limited",
        "Nova Engineering Limited",
        "Prime Infrastructure Private Limited",
    ]

    return random.choice(companies)


def generate_fake_value(pii_type):
    if pii_type == "FULL_NAME":
        return generate_fake_name()

    if pii_type == "EMAIL":
        return generate_fake_email()

    if pii_type == "PHONE":
        return generate_fake_phone()

    if pii_type == "PHYSICAL_ADDRESS":
        return generate_fake_address()

    if pii_type == "COMPANY_NAME":
        return generate_fake_company()

    if pii_type == "IP_ADDRESS":
        return "192.0.2.1"

    if pii_type == "SSN":
        return "000-00-0000"

    if pii_type == "CREDIT_CARD":
        return "4111 1111 1111 1111"

    if pii_type in ("DOB", "DATE_OF_BIRTH"):
        return "01/01/1990"

    return "[REDACTED]"