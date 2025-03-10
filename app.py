from flask import Flask, render_template, flash, redirect, url_for, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
import sys
import pandas as pd
import logging
import shutil
import importlib.util

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add UP directory to Python path
UP_DIR = os.path.join(os.path.dirname(__file__), 'UP')
if UP_DIR not in sys.path:
    sys.path.append(UP_DIR)

# Try to import ContactExtractor
try:
    from contact_extractor import ContactExtractor
    logger.info("Successfully imported ContactExtractor")
except ImportError as e:
    logger.error(f"Failed to import ContactExtractor: {str(e)}")
    # Try alternative import method
    try:
        spec = importlib.util.spec_from_file_location(
            "contact_extractor",
            os.path.join(UP_DIR, "contact_extractor.py")
        )
        contact_extractor_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(contact_extractor_module)
        ContactExtractor = contact_extractor_module.ContactExtractor
        logger.info("Successfully imported ContactExtractor using alternative method")
    except Exception as e:
        logger.error(f"Failed to import ContactExtractor using alternative method: {str(e)}")

# Project list - can be moved to a configuration file later
PROJECTS = [
    {
        'id': 'contact-extractor',
        'name': 'מחלץ אנשי קשר',
        'description': 'חילוץ אנשי קשר מקבצי Excel ו-Word',
        'route': '/contact-extractor'
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
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html', PROJECTS=PROJECTS)

@app.route('/pdf-editor')
def pdf_editor():
    return render_template('pdf_editor.html', PROJECTS=PROJECTS)

@app.route('/robotic-parking')
def robotic_parking():
    return render_template('robotic_parking.html', PROJECTS=PROJECTS)

@app.route('/contact-extractor')
def contact_extractor():
    return render_template('contact_extractor.html', PROJECTS=PROJECTS)

@app.route('/contact-extractor/process', methods=['POST'])
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
        
        # יצירת מחלץ אנשי קשר
        extractor = ContactExtractor()
        
        # עיבוד הקובץ
        if filename.lower().endswith(('.xlsx', '.xls')):
            contacts = extractor.extract_from_xlsx(filepath)
        else:
            contacts = extractor.extract_from_doc(filepath)
        
        if not contacts:
            return jsonify({'success': False, 'error': 'לא נמצאו אנשי קשר בקובץ'})
        
        # שמירת התוצאות
        output_filename = f"processed_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # המרת התוצאות לקובץ Excel
        df = pd.DataFrame([{
            'שם': contact.name,
            'טלפון': '; '.join(contact.phones) if contact.phones else '',
            'אימייל': '; '.join(contact.emails) if contact.emails else '',
            'כתובת': '; '.join(contact.addresses) if contact.addresses else '',
            'קובץ מקור': filename
        } for contact in contacts])
        
        df.to_excel(output_filepath, index=False)
        
        return jsonify({
            'success': True,
            'count': len(contacts),
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