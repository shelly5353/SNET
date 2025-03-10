from flask import Flask, render_template, flash, redirect, url_for, request, send_file
import os
from werkzeug.utils import secure_filename
import subprocess
import sys

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key in production

# Project list - can be moved to a configuration file later
PROJECTS = [
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
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process the file using the UP application
        try:
            # Get the absolute path to the UP application
            up_app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'UP')
            
            # Run the UP application with the uploaded file
            result = subprocess.run([sys.executable, up_app_path, filepath], 
                                 capture_output=True, 
                                 text=True)
            
            if result.returncode == 0:
                flash('File processed successfully!')
            else:
                flash(f'Error processing file: {result.stderr}')
        except Exception as e:
            flash(f'Error running UP application: {str(e)}')
        
        return redirect(url_for('up'))
    
    flash('File type not allowed')
    return redirect(request.url)

if __name__ == '__main__':
    app.run(debug=True, port=3000, host='0.0.0.0') 