from flask import Flask, render_template, request, send_file
import os
from pdf2image import convert_from_path
import pytesseract
import camelot
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Route: Upload PDF
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["pdf"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # --- Step 1: Convert PDF pages to text via OCR ---
        pages = convert_from_path(filepath, dpi=300)
        text_pages = []
        for page in pages:
            text = pytesseract.image_to_string(page)
            text_pages.append(text)

        # --- Step 2: Extract tables using Camelot ---
        try:
            tables = camelot.read_pdf(filepath, pages="all")
            tables_preview = [t.df.to_html() for t in tables]
        except Exception as e:
            tables_preview = []

        # Show preview (text + tables)
        return render_template(
            "preview.html",
            text_pages=text_pages,
            tables=tables_preview,
            filename=file.filename
        )
    return render_template("upload.html")

# Route: Confirm & Generate Word File
@app.route("/confirm/<filename>", methods=["POST"])
def confirm(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Convert to images & run OCR again
    pages = convert_from_path(filepath, dpi=300)
    doc = Document()

    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        doc.add_paragraph(text)

    # Extract tables & add to Word
    try:
        tables = camelot.read_pdf(filepath, pages="all")
        for t in tables:
            table = doc.add_table(rows=0, cols=len(t.df.columns))
            for row in t.df.values.tolist():
                cells = table.add_row().cells
                for j, val in enumerate(row):
                    cells[j].text = str(val)
    except:
        pass

    output_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", ".docx"))
    doc.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
