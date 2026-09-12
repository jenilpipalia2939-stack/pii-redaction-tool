import os
import tempfile
import shutil
from pathlib import Path

from flask import Flask, render_template, request, send_file, after_this_request

from src.main import detect_all_pii, create_docx
from src.extractor import extract_text_from_pdf
from src.redactor import redact_text


app = Flask(__name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        uploaded_file = request.files.get("file")

        if not uploaded_file or uploaded_file.filename == "":
            return render_template(
                "index.html",
                error="Please select a PDF file."
            )

        if not allowed_file(uploaded_file.filename):
            return render_template(
                "index.html",
                error="Only PDF files are supported."
            )

        temp_dir = tempfile.mkdtemp()

        input_path = Path(temp_dir) / "input.pdf"
        output_path = Path(temp_dir) / "redacted_output.docx"

        try:

            uploaded_file.save(input_path)

            # Extract PDF text
            text = extract_text_from_pdf(input_path)

            # Detect PII
            detections = detect_all_pii(text)

            # Redact detected PII
            redacted_text, _ = redact_text(text, detections)

            # Generate DOCX
            create_docx(redacted_text, output_path)

            @after_this_request
            def cleanup(response):
                shutil.rmtree(temp_dir, ignore_errors=True)
                return response

            return send_file(
                output_path,
                as_attachment=True,
                download_name="redacted_document.docx",
                mimetype=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                )
            )

        except Exception as error:

            shutil.rmtree(temp_dir, ignore_errors=True)

            return render_template(
                "index.html",
                error=f"Processing failed: {error}"
            )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)