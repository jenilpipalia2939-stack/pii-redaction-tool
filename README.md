# PII Redaction Tool

A Python-based PII redaction tool that extracts text from PDF documents, detects supported Personally Identifiable Information (PII), replaces detected values with synthetic alternatives, and generates a redacted DOCX document.

## Assignment

**FDE Intern Assignment — PII Redaction Tool**

The tool was developed to process the supplied document and redact sensitive personal and organizational information while maintaining consistent synthetic replacements for repeated values.

---

## Features

* PDF text extraction using PyMuPDF
* Rule-based PII detection using Python regular expressions
* Validation for IP addresses
* Luhn validation for credit card numbers
* Context/rule-based detection for names, companies and physical addresses
* Synthetic PII replacement
* Consistent replacement for repeated PII values
* DOCX output generation
* Automated detector tests using pytest
* End-to-end leakage verification

---

## Supported PII

The detector supports the following categories:

| PII Type           | Detection |
| ------------------ | --------- |
| Full Name          | Yes       |
| Email Address      | Yes       |
| Phone Number       | Yes       |
| Company Name       | Yes       |
| Physical Address   | Yes       |
| SSN                | Yes       |
| Credit Card Number | Yes       |
| Date of Birth      | Yes       |
| IP Address         | Yes       |

The supplied prospectus primarily contains names, email addresses, phone numbers, company names and physical addresses.

---

## Technology Stack

* **Python 3.10+**
* **PyMuPDF** — PDF text extraction
* **python-docx** — DOCX generation and reading
* **pytest** — automated testing
* **Regular Expressions** — PII pattern detection
* **Python `ipaddress` module** — IP validation

No external PII/NLP service is required for the core redaction pipeline.

---

## Project Structure

```text
pii-redaction-tool/
│
├── evaluation/
│   └── evaluation.md
│
├── input/
│   └── prospectus.pdf
│
├── output/
│   └── redacted_prospectus.docx
│
├── src/
│   ├── detectors.py
│   ├── extractor.py
│   ├── faker.py
│   ├── main.py
│   ├── normalizer.py
│   └── redactor.py
│
├── tests/
│   ├── test_detectors.py
│   └── test_redactor.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

The supplied source PDF and generated DOCX are excluded from Git through `.gitignore`.

---

## How It Works

The processing pipeline is:

```text
                PDF
                 │
                 ▼
        Text Extraction
          using PyMuPDF
                 │
                 ▼
        Text Normalization
                 │
                 ▼
          PII Detection
                 │
       ┌─────────┴─────────┐
       │                   │
   Regex Rules       Context Rules
       │                   │
       └─────────┬─────────┘
                 ▼
         PII Detections
                 │
                 ▼
        Synthetic Values
                 │
                 ▼
        Text Redaction
                 │
                 ▼
          DOCX Generation
                 │
                 ▼
       Redacted DOCX Output
```

### 1. Text extraction

The PDF is opened using PyMuPDF and text is extracted page by page.

PDF block extraction is used to improve handling of the document's layout and line breaks.

### 2. PII detection

Different detection strategies are used depending on the PII category.

Examples:

* Emails use email-pattern matching.
* Phone numbers use supported Indian phone-number formats.
* IP addresses are validated using Python's IP address parser.
* Credit-card candidates are validated using the Luhn algorithm.
* Full names use a precision-oriented known-name/rule approach.
* Company names use known company patterns and legal-suffix rules.
* Physical addresses use document-aware address patterns.

### 3. Synthetic replacement

Detected PII is replaced with synthetic values.

For repeated PII values, the tool maintains a replacement map so that the same original value receives the same replacement.

For example:

```text
Original:
Rajesh Kushal Hegde

First occurrence:
Aarav Mehta

Later occurrences:
Aarav Mehta
```

The exact synthetic value is generated automatically by the application.

### 4. DOCX generation

The redacted text is written into:

```text
output/redacted_prospectus.docx
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/jenilpipalia2939-stack/pii-redaction-tool.git
cd pii-redaction-tool
```

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Tool

Place the source PDF at:

```text
input/prospectus.pdf
```

Then run:

```bash
python -m src.main
```

The processed document will be generated at:

```text
output/redacted_prospectus.docx
```

The terminal also displays a PII detection summary.

Example:

```text
PII Detection Summary
------------------------------
EMAIL: 52
PHONE: 32
FULL_NAME: 135
COMPANY_NAME: 185
PHYSICAL_ADDRESS: 10
------------------------------
Total detections: 414
```

The exact counts can change if the input document changes.

---

## Running Tests

Run:

```bash
pytest -q
```

The current automated test suite contains 27 tests.

Latest result:

```text
27 passed
```

The tests cover:

* Valid PII detection
* Invalid PII rejection
* PII type classification
* Formatting variations
* PDF extraction-related line breaks
* Credit-card validation
* IP validation
* Company detection
* Name detection
* Redaction behavior
* Consistent replacement behavior

---

## Evaluation

The evaluation uses two levels:

### Detector-level evaluation

A curated test dataset is used to calculate precision and recall.

The current test fixtures produced:

| Metric          | Result |
| --------------- | -----: |
| True Positives  |     22 |
| False Positives |      0 |
| False Negatives |      0 |
| Precision       |   100% |
| Recall          |   100% |

These values apply specifically to the curated automated test fixtures and should not be interpreted as universal real-world PII detection accuracy.

### End-to-end validation

The supplied prospectus was processed through the complete pipeline.

Final validation:

```text
Original unique PII values detected: 182
Potential leaked values: 0
```

This means none of the 182 unique PII values detected by the application's detectors were found in the generated DOCX during the leakage check.

For the complete methodology and discussion of false positives, false negatives and limitations, see:

```text
evaluation/evaluation.md
```

---

## Design Decisions

### Why regex and rules?

The assignment can be implemented without requiring a large NLP model or external PII service.

A rule-based approach provides:

* Simple deployment
* Predictable behavior
* Easy debugging
* Low resource usage
* No external API dependency

### Why document-aware rules?

Names, company names and addresses are highly context-dependent.

A completely generic capitalized-word pattern can incorrectly classify ordinary document text as a person's name.

For the supplied prospectus, document-aware rules were used to improve precision.

This is a deliberate tradeoff between:

**Precision for the supplied document**

and

**Generalization to arbitrary documents.**

---

## Limitations

This is a lightweight rule-based PII redaction system and is not intended to replace production-grade PII detection systems.

Known limitations include:

* Unusual names may not be detected.
* Company names with uncommon formats may be missed.
* Addresses can have many possible structures.
* Scanned/image-only PDFs require OCR before text-based detection can work.
* PDF extraction can introduce unexpected line breaks.
* The generated DOCX does not preserve all original PDF formatting.
* Document-specific rules improve precision for the supplied document but reduce generalization.
* Regex-based detection cannot fully understand semantic context.
* The evaluation dataset is smaller than a production-scale PII benchmark.

---

## Privacy Considerations

The supplied prospectus contains real-looking personal and organizational information.

The original PDF is intentionally excluded from the Git repository.

The `.gitignore` contains:

```text
input/prospectus.pdf
output/*.docx
```

Therefore, the source document and generated output should be shared separately rather than committed to the public repository.

---

## Future Improvements

Possible improvements for a production-oriented implementation include:

* Named Entity Recognition using a dedicated NLP model
* Microsoft Presidio or another specialized PII framework
* OCR support for scanned PDFs
* Better address and organization recognition
* Preservation of original document formatting
* Confidence scores for detections
* Human review workflow for low-confidence detections
* Batch document processing
* Additional international phone/address formats
* More comprehensive benchmark datasets

---

## Author

**Jenil Pipaliya**

GitHub:

https://github.com/jenilpipalia2939-stack
