
from pathlib import Path

from docx import Document

from src.extractor import extract_text_from_pdf
from src.detectors import (
    detect_emails,
    detect_phone_numbers,
    detect_ip_addresses,
    detect_ssn,
    detect_credit_cards,
    detect_dates_of_birth,
    detect_full_names,
    detect_company_names,
    detect_physical_addresses,
)
from src.redactor import redact_text


INPUT_PDF = "input/prospectus.pdf"
OUTPUT_DOCX = "output/redacted_prospectus.docx"


def detect_all_pii(text):
    detections = []

    detections.extend(detect_emails(text))
    detections.extend(detect_phone_numbers(text))
    detections.extend(detect_ip_addresses(text))
    detections.extend(detect_ssn(text))
    detections.extend(detect_credit_cards(text))
    detections.extend(detect_dates_of_birth(text))
    detections.extend(detect_full_names(text))
    detections.extend(detect_company_names(text))
    detections.extend(detect_physical_addresses(text))

    return detections


def print_summary(detections):
    counts = {}

    for detection in detections:
        pii_type = detection["type"]
        counts[pii_type] = counts.get(pii_type, 0) + 1

    print("\nPII Detection Summary")
    print("-" * 30)

    for pii_type, count in counts.items():
        print(f"{pii_type}: {count}")

    print("-" * 30)
    print(f"Total detections: {len(detections)}")


def create_docx(text, output_path):
    """
    Create a DOCX document from the redacted text.
    """

    output_file = Path(output_path)

    # Create output directory if it does not exist.
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    document = Document()

    # Split the extracted text into paragraphs.
    paragraphs = text.split("\n\n")

    for paragraph_text in paragraphs:
        paragraph_text = paragraph_text.strip()

        if paragraph_text:
            document.add_paragraph(paragraph_text)

    document.save(output_file)


def main():
    print("Starting PII Redaction Tool...")
    print()

    # ---------------------------------------------------------
    # 1. Extract text
    # ---------------------------------------------------------
    print("1. Extracting text from PDF...")

    text = extract_text_from_pdf(INPUT_PDF)

    print(f"Extracted characters: {len(text)}")

    # ---------------------------------------------------------
    # 2. Detect PII
    # ---------------------------------------------------------
    print()
    print("2. Detecting PII...")

    detections = detect_all_pii(text)

    print_summary(detections)

    # ---------------------------------------------------------
    # 3. Redact PII
    # ---------------------------------------------------------
    print()
    print("3. Redacting PII...")

    redacted_text, replacement_map = redact_text(
        text,
        detections
    )

    print(f"Unique replacements: {len(replacement_map)}")

    # ---------------------------------------------------------
    # 4. Generate DOCX
    # ---------------------------------------------------------
    print()
    print("4. Generating DOCX...")

    create_docx(
        redacted_text,
        OUTPUT_DOCX
    )

    print(f"Redacted DOCX saved to: {OUTPUT_DOCX}")

    print()
    print("PII redaction completed successfully.")


if __name__ == "__main__":
    main()

