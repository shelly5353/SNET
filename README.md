# SNET - Shelly's Project Storage Site

SNET is a centralized platform for storing, displaying, and running various development projects.

## Setup Instructions / הוראות התקנה

### Create Virtual Environment / יצירת סביבה וירטואלית
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Install Dependencies / התקנת ספריות
```bash
pip install -r requirements.txt
```

### Run the Application / הרצת האפליקציה
```bash
python app.py
```
The application will be available at `http://localhost:5000`

## Project Structure / מבנה הפרויקט
```
SNET/
├── app.py                    # Flask application
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   └── project_page.html    # Project template
├── static/                 # Static files
│   └── style.css           # CSS styles
└── README.md               # This file
```

## Adding New Projects / הוספת פרויקטים חדשים

1. Create a new HTML file in the `templates` directory using `project_page.html` as a template
2. Add the project route in `app.py`
3. Add the project card to `index.html`

## Development / פיתוח

The site uses Flask for the backend and plain HTML/CSS for the frontend. The design follows a dark mode theme with a clean, minimalist interface. 