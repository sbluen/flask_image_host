# Flask Image Host

A Flask-based web application for image hosting with user authentication and image gallery management.

## Features

- User registration and authentication
- Secure image upload with validation
- Personal image gallery
- Image metadata (title, description)
- Responsive design
- SQLite database for data persistence

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd flask_image_host
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Run the development server**:
   ```bash
   python run.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Create an account** and start uploading images!

## Project Structure

```
flask_image_host/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models (User, Image)
│   ├── routes.py            # Application routes
│   ├── forms.py             # WTForms form definitions
│   └── templates/           # HTML templates
│       ├── base.html        # Base template
│       ├── index.html       # Home page
│       ├── gallery.html     # User gallery
│       ├── upload.html      # Image upload form
│       ├── login.html       # Login page
│       └── register.html    # Registration page
├── static/
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   └── script.js        # Client-side JavaScript
│   └── uploads/             # Uploaded images directory
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md               # This file
```

## Dependencies

- **Flask**: Web framework
- **Flask-SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling with CSRF protection
- **Werkzeug**: File handling and security utilities
- **WTForms**: Form validation

## Configuration

Edit `config.py` to customize:
- Database URI
- File upload limits
- Session timeout
- Security settings

## Security Notes

- Change `SECRET_KEY` in `config.py` for production
- Set `SESSION_COOKIE_SECURE = True` when using HTTPS
- Set `WTF_CSRF_SSL_STRICT = True` in production
- Ensure proper file permissions on upload directory

## Allowed Image Formats

- PNG
- JPG/JPEG
- GIF
- WebP

Maximum file size: 16MB

## Troubleshooting

- **Database errors**: Delete `instance/image_host.db` and restart to reinitialize
- **Upload fails**: Check `static/uploads/` directory exists and is writable
- **Port 5000 in use**: Change `port=5000` in `run.py` to another port

## Development

For development mode with hot reload, ensure `debug=True` in `run.py`.

## License

This project is open source and available under the MIT License.
