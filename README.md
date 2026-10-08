# Digital Gram Panchayat

A smart, web-based digital governance and citizen service management platform designed to simplify public service access in rural and semi-urban communities. The system connects citizens, staff, and administrators in a single digital workflow for service requests, approvals, tracking, and monitoring.

The project is designed as a practical e-governance solution for village administration and public service delivery.

## Project Vision

The Digital Gram Panchayat platform aims to reduce reliance on paperwork, manual recordkeeping, and delayed approvals by providing a centralized digital system for village services. It enables citizens to register, request services, and track their application status while allowing staff and administrators to review and process requests efficiently.

## Problem Statement

In many rural and local governance environments, public service delivery still depends heavily on manual processes, paper records, and fragmented administrative systems. This leads to:

- Long queues and slow service processing
- Difficulties in tracking applications or requests
- Increased risk of missing important records
- Poor transparency between citizens and administrators
- Lack of accountability in decision-making and follow-up
- Higher administrative workload and reduced efficiency

Digital Gram Panchayat addresses these issues by digitizing the service workflow and making governance more transparent and citizen-friendly.

## Objectives

- Digitize village-level public service management
- Improve transparency and accountability in local governance
- Reduce manual paperwork and delays in processing
- Provide a centralized system for applications and status tracking
- Enable role-based access for citizens, staff, and administrators
- Improve citizen engagement with public services
- Build a scalable foundation for future e-governance features

## Key Features

### Citizen Features
- User registration and login
- Profile management
- Service catalog listing available services
- Application submission workflow
- Tracking of application status
- Dashboard for citizen activity overview
- Notification support for service updates

### Staff Features
- Review submitted applications
- Update application status
- Approve or reject requests
- Add administrative notes
- View pending and processed items
- Manage everyday public service requests efficiently

### Admin Features
- Add and manage available services
- Monitor system-wide statistics
- Review recent applications
- Validate platform activity and workflow performance
- Maintain governance transparency at the administrative level

### General Features
- Role-based access control
- Responsive UI for better usability
- Secure password handling
- Modular backend architecture
- SQLite database support for lightweight deployment
- Dashboard-based monitoring and reporting

## Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Backend
- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- WTForms / Flask-WTF

### Database
- SQLite

## System Architecture

The project follows a modular Flask architecture:

- Routes handle user interaction and page rendering
- Models define the database schema
- Forms validate user input and application data
- Config holds project configuration values
- Templates render the user interface
- SQLite stores application and user data

## Application Workflow

1. Citizen registers and logs in
2. Citizen browses available services
3. Citizen submits a service request/application
4. Staff/Admin reviews the request
5. Application status is updated
6. Citizen can view the current status in the dashboard
7. Administrative monitoring continues across all requests

## Roles in the System

### 1. Citizen
- Register an account
- Apply for services
- Track application status
- View personal profile

### 2. Staff
- Review applications submitted by citizens
- Approve or reject service requests
- Maintain workflow status and notes

### 3. Admin
- Add services
- Monitor applications and user data
- Maintain central administrative control

## Project Structure

```text
Digital-Gram-Panchayat-Python/
│
├── app.py
├── config.py
├── forms.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── services.html
│   ├── service_detail.html
│   ├── my_applications.html
│   ├── profile.html
│   ├── admin_dashboard.html
│   ├── staff_dashboard.html
│   ├── review_application.html
│   ├── add_service.html
│   ├── 404.html
│   └── 500.html
│
└── instance/
    └── gram_panchayat.db
```

## Core Database Models

The application manages important entities such as:

- User
- Service
- Application
- Notification
- AuditLog
- ServiceCategory
- SystemSetting

These models form the foundation for the digital governance workflow.

## Default Admin Credentials

```text
Email: admin@panchayat.in
Password: Admin@123
```

## Installation Guide

### Prerequisites

- Python 3.10 or above
- pip
- Virtual environment support

### Setup Steps

```bash
git clone https://github.com/viraj24bce10396/Digital-Gram-Panchayat-Python.git
cd Digital-Gram-Panchayat-Python
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open the app in your browser at:

```text
http://localhost:5000
```

## Screenshots

> Add project screenshots here for presentation and documentation purposes.
> These can be captured after running the app locally and inserted into the folder shown below.

```text
docs/screenshots/
├── home-page.png
├── login-page.png
├── registration-page.png
├── dashboard.png
├── services-page.png
├── admin-dashboard.png
├── staff-review-page.png
```

Example usage in README:

```md
![Home Page](docs/screenshots/home-page.png)
![Login Page](docs/screenshots/login-page.png)
![Dashboard](docs/screenshots/dashboard.png)
```

## Sample UI Flow

- Home page for public access
- User registration page
- Login page
- Citizen dashboard showing available services
- Service request form
- Staff/admin review page
- Final status tracking on the citizen side

## Benefits of the Project

- Reduces paper-based dependency
- Improves citizen access to public services
- Makes service processing more transparent
- Supports easier monitoring and administration
- Enables scalable digital governance
- Creates a real-world example of public sector digitization

## Future Enhancements

This project can be extended with:

- Document upload support
- PDF generation for certificates and approvals
- SMS and email notifications
- Advanced analytics dashboard
- Multilingual interface support
- Mobile-first experience
- Geographic mapping of citizen requests
- Integration with external government systems

## Real-World Impact

Digital Gram Panchayat demonstrates how modern web technologies can be used to improve governance and make public service delivery more accessible, accountable, and efficient. The platform helps local administration function more smoothly while improving the experience for citizens who rely on public services.

## Conclusion

Digital Gram Panchayat is a practical, academic, and socially relevant project that combines software engineering with e-governance. It highlights how technology can transform traditional administrative workflows into transparent, digital-first systems that better serve communities.

## Acknowledgements

- Flask community
- Bootstrap team
- Python ecosystem contributors
- Open-source contributors and academic mentors

## License

This project is intended for educational, academic, and demonstration purposes.

## Project Status

Status: Working prototype / academic project

## Contact / Author

Digital Gram Panchayat
Academic Project

---

This project is designed to be both technically functional and presentation-ready for academic evaluation.

