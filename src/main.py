from detectors import detect_emails


text_file_path = "output/extracted_text.txt"

with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()


emails = detect_emails(text)

print(f"Emails detected: {len(emails)}")

for email in emails[:20]:
    print(email)