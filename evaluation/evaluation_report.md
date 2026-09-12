# PII Redaction Tool — Evaluation Report

## 1. Objective

The objective of this evaluation is to measure the effectiveness of the PII Redaction Tool in:

1. Detecting supported PII categories.
2. Avoiding false detections on normal non-PII text.
3. Replacing detected PII with synthetic values.
4. Maintaining consistent replacements for repeated PII values.
5. Ensuring that detected original PII does not remain in the generated DOCX.

The evaluation uses both automated unit tests and an end-to-end validation of the supplied prospectus document.

---

## 2. Supported PII Categories

The implementation currently supports detection of:

* Full names
* Email addresses
* Phone numbers
* Company names
* Physical addresses
* SSNs
* Credit card numbers
* Dates of birth
* IP addresses

The supplied prospectus primarily contains names, email addresses, phone numbers, company names and physical addresses. The remaining categories are covered through unit tests.

---

## 3. Evaluation Strategy

The evaluation consists of two levels.

### A. Detector-level evaluation

A curated automated test suite contains positive and negative examples for the supported PII detectors.

Positive examples contain known PII values where the expected result is explicitly defined.

Negative examples contain normal text or invalid PII-like values where the detector is expected to return no match.

The test suite verifies:

* Correct detection
* Correct PII type
* Correct normalized value
* Rejection of invalid formats
* Handling of line breaks introduced by PDF extraction
* Handling of repeated names
* Company-name matching
* Credit-card validation using the Luhn algorithm
* IP address validation

### B. End-to-end document evaluation

The supplied prospectus is processed through the complete pipeline:

```text
PDF
 ↓
Text extraction
 ↓
PII detection
 ↓
PII replacement
 ↓
DOCX generation
 ↓
Leakage verification
```

After generating the DOCX, all unique PII values detected in the original document are searched for in the generated output.

---

## 4. Automated Test Results

The final automated test suite contains:

**27 tests**

Result:

```text
27 passed
```

Therefore:

* Passed: 27
* Failed: 0
* Test pass rate: 100%

The positive test fixtures contain **22 expected PII entities** across the supported detector categories.

The negative test fixtures contain invalid PII-like values and ordinary non-PII text.

### Detector metrics on the curated test fixtures

| Metric          | Result |
| --------------- | -----: |
| True Positives  |     22 |
| False Positives |      0 |
| False Negatives |      0 |
| Precision       |   100% |
| Recall          |   100% |

### Calculations

Precision:

```text
TP / (TP + FP)
= 22 / (22 + 0)
= 100%
```

Recall:

```text
TP / (TP + FN)
= 22 / (22 + 0)
= 100%
```

These results apply only to the explicitly curated unit-test dataset. They should not be interpreted as a guarantee of 100% precision or recall on arbitrary documents.

---

## 5. End-to-End Document Results

The supplied prospectus was processed using the complete redaction pipeline.

Final detection summary:

| PII Type         | Detections |
| ---------------- | ---------: |
| Email            |         52 |
| Phone            |         32 |
| Full Name        |        135 |
| Company Name     |        185 |
| Physical Address |         10 |
| **Total**        |    **414** |

The tool generated:

```text
output/redacted_prospectus.docx
```

The redaction process produced **175 unique replacement mappings**.

---

## 6. Leakage Verification

A separate verification was performed after generating the DOCX.

The verification:

1. Extracted the original PDF text.
2. Ran the complete PII detector.
3. Collected the unique detected PII values.
4. Extracted text from the generated DOCX.
5. Checked whether any original detected PII value remained in the output.

Final result:

```text
Original unique PII values detected: 182
Potential leaked values: 0
```

Therefore, **0 of the 182 unique detected PII values were found in the generated DOCX during this verification.**

This provides an end-to-end validation that the detected PII values were successfully replaced in the generated text output.

---

## 7. False Positives

False positives occur when normal text is incorrectly identified as PII.

The implementation uses several precision-oriented rules to reduce this problem.

### Examples

#### Phone numbers

The detector does not classify every long number as a phone number. It looks for supported phone-number patterns.

#### IP addresses

The detector additionally validates detected IPv4 values using Python's IP address validation.

#### Credit cards

Potential card numbers are validated using the Luhn algorithm before being classified as credit cards.

#### Full names

A generic capitalized-word detector can incorrectly classify ordinary text such as headings or phrases as names.

To improve precision for the supplied prospectus, the implementation uses a document-specific known-name list rather than treating every capitalized phrase as a person.

#### Company names

Company detection uses known company names together with a generic legal-suffix pattern.

Additional filtering prevents legal suffixes such as:

```text
Private Limited
Limited
LLP
```

from being classified as complete company names by themselves.

---

## 8. False Negatives

False negatives occur when actual PII exists but is not detected.

The main causes that may produce false negatives include:

* Unusual formatting
* OCR errors
* Images containing PII rather than selectable text
* Names not included in the document-specific known-name list
* Company names using uncommon legal suffixes
* Addresses with unusual layouts
* PII split across PDF text blocks in unexpected ways
* PII formats not covered by the current regular expressions

The supplied prospectus contains complex PDF layouts and line breaks. The implementation therefore includes normalization and patterns that account for some extraction-related formatting issues.

However, this remains a regex/rule-based solution and is not intended to provide universal PII recognition.

---

## 9. Replacement Consistency

Repeated PII values should receive the same synthetic replacement.

The redactor maintains a replacement map.

For example:

```text
Original:
Rajesh Kushal Hegde

Replacement:
<synthetic name>
```

Every subsequent occurrence of the same normalized full name uses the same replacement.

Full-name keys are normalized case-insensitively to improve consistency when the same name appears with different capitalization.

---

## 10. Security and Privacy Considerations

The original prospectus contains real-looking personal and organizational information.

The original PDF is intentionally excluded from the Git repository using `.gitignore`.

The repository therefore contains the processing code and documentation rather than the supplied source document.

The generated DOCX should be shared separately using controlled access.

---

## 11. Limitations

This implementation intentionally uses a lightweight regex and rule-based approach.

It does not use a trained Named Entity Recognition model.

Important limitations include:

1. Context-dependent names can be difficult to distinguish from ordinary text.
2. Company names may use formats not covered by the current rules.
3. Addresses can have many possible structures.
4. Scanned/image-only PDFs require OCR before text-based detection can work.
5. Formatting information from the original PDF is not fully preserved in the generated DOCX.
6. Document-specific known-name and company lists improve precision for this assignment but reduce generality.
7. The evaluation dataset is relatively small compared with a production PII benchmark.

---

## 12. Conclusion

The final implementation successfully completed the supplied-document redaction workflow.

The verified results are:

* **27/27 automated tests passed**
* **414 PII occurrences detected in the supplied prospectus**
* **182 unique detected PII values checked**
* **0 potential detected-PII leaks in the generated DOCX**
* Synthetic replacements generated for detected PII
* Repeated PII values maintain consistent replacements

The detector-level precision and recall were both 100% on the curated automated test fixtures. The end-to-end leakage test additionally confirmed that none of the 182 unique detected original PII values remained in the generated DOCX.

The metrics should be interpreted within the scope of the documented evaluation dataset and the rule-based nature of the implementation.
