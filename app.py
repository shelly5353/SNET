from flask import Flask, render_template, flash, redirect, url_for, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
import sys
import pandas as pd
import logging
import shutil

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Project list - can be moved to a configuration file later
PROJECTS = [
    {
        'id': 'up',
        'name': 'UP Application',
        'description': 'Process and analyze files using the UP application',
        'route': '/up'
    },
    {
        'id': 'pdf-editor',
        'name': 'PDF Editor',
        'description': 'Edit and manipulate PDF files easily',
        'route': '/pdf-editor'
    },
    {
        'id': 'robotic-parking',
        'name': 'Robotic Parking Simulator',
        'description': 'Simulation of an automated parking system',
        'route': '/robotic-parking'
    }
]

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'csv', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', projects=PROJECTS)

@app.route('/pdf-editor')
def pdf_editor():
    return render_template('pdf_editor.html', PROJECTS=PROJECTS)

@app.route('/robotic-parking')
def robotic_parking():
    return render_template('robotic_parking.html', PROJECTS=PROJECTS)

@app.route('/up')
def up():
    return render_template('up.html')

@app.route('/up/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'לא נבחר קובץ'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'לא נבחר קובץ'})
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'סוג קובץ לא נתמך'})
    
    try:
        # שמירת הקובץ
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # העתקת הקובץ לתיקיית UP
        up_dir = os.path.join(os.path.dirname(__file__), 'UP')
        target_filepath = os.path.join(up_dir, filename)
        shutil.copy2(filepath, target_filepath)
        
        # הוספת תיקיית UP ל-PYTHONPATH
        sys.path.append(up_dir)
        
        # ייבוא המודולים הנדרשים
        from read_docs import process_file as process_doc
        from contact_extractor import ContactExtractor
        
        # עיבוד הקובץ בהתאם לסוגו
        if filename.lower().endswith(('.doc', '.docx')):
            process_doc(target_filepath)
        else:
            extractor = ContactExtractor()
            extractor.extract_from_xlsx(target_filepath)
        
        # העתקת קובץ התוצאות
        output_filename = f"processed_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        shutil.copy2(os.path.join(up_dir, 'Data_Base.xlsx'), output_filepath)
        
        # ספירת מספר אנשי הקשר שנמצאו
        df = pd.read_excel(output_filepath)
        count = len(df)
        
        return jsonify({
            'success': True,
            'count': count,
            'output_file': url_for('uploaded_file', filename=output_filename)
        })
        
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return jsonify({'success': False, 'error': f'שגיאה: {str(e)}'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0') 