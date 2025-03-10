from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
from contact_extractor import ContactExtractor

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure allowed file extensions
ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact-extractor')
def contact_extractor():
    return render_template('contact_extractor.html')

@app.route('/contact-extractor/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload an Excel or Word file.'})
    
    try:
        # Create a unique filename to avoid conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{os.urandom(8).hex()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        extractor = ContactExtractor()
        contacts = extractor.extract_from_file(filepath)
        
        if not contacts:
            return jsonify({'success': False, 'error': 'No contacts found in the file'})
        
        # Save contacts to Excel file with unique name
        output_filename = f'contacts_{unique_filename}.xlsx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        extractor.save_contacts_to_excel(contacts, output_path)
        
        return jsonify({
            'success': True,
            'contacts_count': len(contacts),
            'output_file': f'/download/{output_filename}'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass  # Ignore cleanup errors

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    finally:
        # Clean up the output file after download
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except:
            pass  # Ignore cleanup errors

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 