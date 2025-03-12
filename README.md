# SNET - Shelly's Project Storage Site

SNET is a centralized platform for storing, displaying, and running various development projects.

## Setup Instructions / הוראות התקנה

### Create Virtual Environment / יצירת סביבה וירטואלית
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

### Install Dependencies / התקנת ספריות
```bash
pip install -r requirements.txt
```

### Environment Setup / הגדרות סביבה
Copy `.env.example` to `.env` and update the values as needed:
```bash
cp .env.example .env
```

### Run the Application / הרצת האפליקציה
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Project Structure / מבנה הפרויקט
```
SNET/
├── app.py                    # Main Flask application
├── contact_extractor.py      # Contact extraction functionality
├── gunicorn.conf.py         # Gunicorn configuration
├── requirements.txt         # Python dependencies
├── runtime.txt             # Python runtime specification
├── Procfile               # Process file for deployment
├── render.yaml            # Render deployment configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   └── pdf_easy_edits.html # PDF editor page
├── static/              # Static files
│   ├── style.css        # CSS styles
│   └── logo.png         # Site logo
├── uploads/            # Directory for uploaded files
├── logs/              # Application logs
└── README.md          # This file
```

## Development / פיתוח

The site uses Flask for the backend and plain HTML/CSS for the frontend. The design follows a dark mode theme with a clean, minimalist interface.

## Deployment / פריסה

The application is configured for deployment on Render using Gunicorn as the WSGI server. The deployment configuration can be found in `render.yaml`.

## Environment Variables / משתני סביבה

Required environment variables are documented in `.env.example`. Make sure to set these up before running the application.

## Adding New Projects / הוספת פרויקטים חדשים

1. Create a new HTML file in the `templates` directory using `project_page.html` as a template
2. Add the project route in `app.py`
3. Add the project card to `index.html`