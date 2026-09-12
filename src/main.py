from detectors import detect_phone_numbers


text_file_path = "output/extracted_text.txt"

with open(text_file_path, "r", encoding="utf-8") as file:
    text = file.read()


phones = detect_phone_numbers(text)

print(f"Phone numbers detected: {len(phones)}")

for phone in phones:
    print(phone["value"])