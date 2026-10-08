# Digital Gram Panchayat

A modern Python Flask project for village administration, citizen service requests, and staff/admin approval workflows.

## Features
- User registration and login
- Three roles: citizen, staff, admin
- Service catalog for certificates and village services
- Application submission tracking
- Admin dashboard with service management
- Staff dashboard for review and approval
- Clean responsive UI

## Tech Stack
- Python 3.10+
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Flask-WTF
- SQLite
- Bootstrap 5

## Run locally
1. Clone the repo
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the app:
   ```bash
   python app.py
   ```
5. Open in browser:
   ```bash
   http://localhost:5000
   ```

## Default admin
- Email: admin@panchayat.in
- Password: Admin@123
