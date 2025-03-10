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
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'doc', 'docx'}
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
        from contact_extractor import ContactExtractor, save_contacts_to_excel
        
        # יצירת מחלץ אנשי קשר
        extractor = ContactExtractor()
        
        # עיבוד הקובץ
        contacts = {}
        if filename.lower().endswith(('.xlsx', '.xls')):
            new_contacts = extractor.extract_from_xlsx(target_filepath)
        else:
            new_contacts = extractor.extract_from_doc(target_filepath)
        
        # המרת רשימת אנשי קשר למילון
        for contact in new_contacts:
            if contact.is_valid():
                # יצירת מפתח ייחודי
                name_key = contact.name.lower().strip()
                phone_key = list(contact.phones)[0] if contact.phones else ""
                email_key = list(contact.emails)[0] if contact.emails else ""
                key = f"{name_key}_{phone_key}_{email_key}"
                
                # בדיקה אם יש כבר איש קשר דומה
                found_match = False
                for existing_key in contacts:
                    if existing_key.startswith(name_key):
                        contacts[existing_key].merge(contact)
                        found_match = True
                        break
                
                if not found_match:
                    contacts[key] = contact
        
        # שמירת התוצאות
        output_filename = f"processed_{filename}"
        output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        save_contacts_to_excel(contacts, output_filepath)
        
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