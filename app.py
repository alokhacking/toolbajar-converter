from flask import Flask, request, send_file
import os
from pdf2docx import Converter

app = Flask(__name__)

@app.route("/")
def home():
    return "ToolBajar Converter Backend Running"

@app.route("/pdf-to-word", methods=["POST"])
def pdf_to_word():
    pdf = request.files["file"]
    pdf_path = "input.pdf"
    docx_path = "output.docx"

    pdf.save(pdf_path)

    cv = Converter(pdf_path)
    cv.convert(docx_path)
    cv.close()

    return send_file(docx_path, as_attachment=True)
