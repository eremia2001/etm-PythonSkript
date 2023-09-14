from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
from convert_csv_to_json import convert_csv_to_json
from create_structured_csv import create_structured_csv

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        json_data = convert_csv_to_json(filepath)
        
        new_csv_path = filepath.replace('.csv', '_processed.csv')
        created_csv_path = create_structured_csv(json_data, new_csv_path)
        
        return jsonify({'success': True, 'filename': os.path.basename(created_csv_path)})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=5000)
