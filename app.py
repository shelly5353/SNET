from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import logging
from logging.handlers import RotatingFileHandler
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add file handler if not running in debug mode
if not os.environ.get('FLASK_DEBUG'):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

logger.info('Starting application...')

try:
    from contact_extractor import ContactExtractor
    logger.info('Successfully imported ContactExtractor')
except ImportError as e:
    logger.error(f'Failed to import ContactExtractor: {str(e)}')
    logger.error(traceback.format_exc())
    raise

app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))
app.config['GA_MEASUREMENT_ID'] = os.getenv('GA_MEASUREMENT_ID')

# Ensure upload directory exists
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    logger.info(f"Upload directory created/verified at {app.config['UPLOAD_FOLDER']}")
except Exception as e:
    logger.error(f"Failed to create upload directory: {str(e)}")
    logger.error(traceback.format_exc())
    raise

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

@app.route('/pdf-easy-edits')
def pdf_easy_edits():
    """Route for the PDF Easy Edits application."""
    return render_template('pdf_easy_edits.html')

@app.route('/file-compressor')
def file_compressor():
    """Route for the File Compressor application."""
    return render_template('file_compressor.html')

@app.route('/simulator')
def simulator():
    return render_template('simulator.html')

@app.route('/contact-extractor/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        logger.warning('No file part in request')
        return jsonify({'success': False, 'error': 'No file uploaded'})
    
    file = request.files['file']
    if file.filename == '':
        logger.warning('No selected file')
        return jsonify({'success': False, 'error': 'No file selected'})
    
    if not allowed_file(file.filename):
        logger.warning(f'Invalid file type: {file.filename}')
        return jsonify({'success': False, 'error': 'Invalid file type. Please upload an Excel or Word file.'})
    
    try:
        # Create a unique filename to avoid conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{os.urandom(8).hex()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        logger.info(f'Saving uploaded file: {filename} as {unique_filename}')
        file.save(filepath)
        
        logger.info('Creating ContactExtractor instance')
        extractor = ContactExtractor()
        
        logger.info(f'Processing file: {filepath}')
        contacts = extractor.extract_from_file(filepath)
        
        if not contacts:
            logger.warning('No contacts found in file')
            return jsonify({'success': False, 'error': 'No contacts found in the file'})
        
        # Save contacts to Excel file with unique name
        output_filename = f'contacts_{unique_filename}.xlsx'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        logger.info(f'Saving {len(contacts)} contacts to: {output_path}')
        extractor.save_contacts_to_excel(contacts, output_path)
        
        return jsonify({
            'success': True,
            'contacts_count': len(contacts),
            'output_file': f'/download/{output_filename}'
        })
        
    except Exception as e:
        logger.error(f'Error processing file: {str(e)}')
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})
    
    finally:
        # Clean up uploaded file
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                logger.info(f'Cleaned up input file: {filepath}')
            except Exception as e:
                logger.error(f'Failed to clean up input file: {str(e)}')

@app.route('/download/<filename>')
def download_file(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        logger.info(f'Sending file: {filepath}')
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        logger.error(f'Error sending file: {str(e)}')
        logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': 'File not found'})
    finally:
        # Clean up the output file after download
        try:
            os.remove(filepath)
            logger.info(f'Cleaned up output file: {filepath}')
        except Exception as e:
            logger.error(f'Failed to clean up output file: {str(e)}')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    logger.info(f'Starting server on port {port}')
    app.run(host='0.0.0.0', port=port) 