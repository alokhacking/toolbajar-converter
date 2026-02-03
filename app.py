from flask import Flask, request, send_file
import os, subprocess, uuid

app = Flask(__name__)

UPLOAD = "uploads"
OUTPUT = "outputs"
os.makedirs(UPLOAD, exist_ok=True)
os.makedirs(OUTPUT, exist_ok=True)

@app.route("/")
def home():
    return "ToolBajar Converter Backend Running"

def libre_convert(input_path, out_dir, out_type):
    subprocess.run([
        "libreoffice", "--headless",
        "--convert-to", out_type,
        input_path,
        "--outdir", out_dir
    ], check=True)

@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    f = request.files["file"]
    name = str(uuid.uuid4())
    in_path = f"{UPLOAD}/{name}.pdf"
    f.save(in_path)

    libre_convert(in_path, OUTPUT, "docx")
    return send_file(f"{OUTPUT}/{name}.docx", as_attachment=True)

@app.route("/word-to-pdf", methods=["POST"])
def word_to_pdf():
    f = request.files["file"]
    name = str(uuid.uuid4())
    in_path = f"{UPLOAD}/{name}.docx"
    f.save(in_path)

    libre_convert(in_path, OUTPUT, "pdf")
    return send_file(f"{OUTPUT}/{name}.pdf", as_attachment=True)

@app.route("/excel-to-pdf", methods=["POST"])
def excel_to_pdf():
    f = request.files["file"]
    name = str(uuid.uuid4())
    in_path = f"{UPLOAD}/{name}.xlsx"
    f.save(in_path)

    libre_convert(in_path, OUTPUT, "pdf")
    return send_file(f"{OUTPUT}/{name}.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
