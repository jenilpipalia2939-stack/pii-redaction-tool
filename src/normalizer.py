import re


def normalize_text(text):
    """
    Normalize common PDF text-extraction issues
    without removing meaningful line breaks.
    """

    # Fix email addresses split across a line break.
    text = re.sub(
        r'([A-Za-z0-9._%+-]+@[A-Za-z0-9-]+\.co)\s*\n\s*(m)\b',
        r'\1\2',
        text,
        flags=re.IGNORECASE
    )

    return text