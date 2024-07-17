from flask import Flask, render_template, request, redirect, url_for, send_file
from pdf2docx import Converter
import PyPDF2
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        file = request.files['pdf_file']
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)
        output_path = os.path.splitext(input_path)[0] + '.docx'

        cv = Converter(input_path)
        cv.convert(output_path)
        cv.close()

        return send_file(output_path, as_attachment=True)
    return render_template('convert.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        file = request.files['pdf_file']
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        # Add your PDF editing functionality here

        return send_file(input_path, as_attachment=True)
    return render_template('edit.html')

@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        file = request.files['pdf_file']
        pages_to_remove = request.form['pages_to_remove']
        pages_to_remove = list(map(int, pages_to_remove.split(',')))

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)
        output_path = os.path.splitext(input_path)[0] + '_removed.pdf'

        with open(input_path, 'rb') as input_pdf_file:
            reader = PyPDF2.PdfReader(input_pdf_file)
            writer = PyPDF2.PdfWriter()

            for page_num in range(len(reader.pages)):
                if page_num not in pages_to_remove:
                    writer.add_page(reader.pages[page_num])

            with open(output_path, 'wb') as output_pdf_file:
                writer.write(output_pdf_file)

        return send_file(output_path, as_attachment=True)
    return render_template('remove.html')

if __name__ == '__main__':
    app.run(debug=True)
