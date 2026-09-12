from extractor import extract_text_from_pdf


pdf_path = "input/prospectus.pdf"

text = extract_text_from_pdf(pdf_path)

output_path = "output/extracted_text.txt"

with open(output_path, "w", encoding="utf-8") as file:
    file.write(text)

print("PDF text extracted successfully.")
print(f"Characters extracted: {len(text)}")
print(f"Saved to: {output_path}")