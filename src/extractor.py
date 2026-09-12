import pymupdf


def extract_text_from_pdf(pdf_path):
    document = pymupdf.open(pdf_path)

    text_parts = []

    for page in document:
        blocks = page.get_text("blocks", sort=True)

        for block in blocks:
            block_text = block[4].strip()

            if block_text:
                text_parts.append(block_text)

    document.close()

    return "\n\n".join(text_parts)