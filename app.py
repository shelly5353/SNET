from flask import Flask, render_template, flash, redirect, url_for, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import subprocess
import sys
import pandas as pd
import logging

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
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
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
        
        # עיבוד הקובץ באמצעות האפליקציה UP
        sys.path.append(os.path.join(os.path.dirname(__file__), 'UP'))
        from contact_extractor import ContactExtractor
        
        # יצירת מחלץ אנשי קשר
        extractor = ContactExtractor()
        
        # עיבוד הקובץ
        contacts = extractor.extract_from_xlsx(filepath)
        
        if not contacts:
            return jsonify({'success': False, 'error': 'לא נמצאו אנשי קשר בקובץ'})
        
        # הכנת קובץ תוצאות
        output_filename = f"processed_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # המרת רשימת אנשי קשר למילון
        contacts_dict = {}
        for contact in contacts:
            if contact.is_valid():
                key = f"{contact.name}_{list(contact.phones)[0] if contact.phones else ''}_{list(contact.emails)[0] if contact.emails else ''}"
                contacts_dict[key] = contact
        
        # שמירת התוצאות
        from contact_extractor import save_contacts_to_excel
        save_contacts_to_excel(contacts_dict, output_filepath)
        
        return jsonify({
            'success': True,
            'count': len(contacts_dict),
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