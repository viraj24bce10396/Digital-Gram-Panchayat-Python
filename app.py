import os
from datetime import datetime, timedelta
from functools import wraps
import json

import pytz
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from config import Config
from forms import ApplicationReviewForm, LoginForm, RegistrationForm, ServiceForm, UpdateProfileForm
from models import Application, AuditLog, Notification, Service, User, db

app = Flask(__name__)
app.config.from_object(Config)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message_category = "warning"


db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))
            if current_user.role not in roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for("dashboard"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def create_default_admin():
    admin = User.query.filter_by(email="admin@panchayat.in").first()
    if not admin:
        admin = User(
            full_name="System Administrator",
            email="admin@panchayat.in",
            phone="9999999999",
            address="Panchayat Office",
            city="Village",
            pincode="123456",
            role="admin",
        )
        admin.set_password("Admin@123")
        db.session.add(admin)
        db.session.commit()


def create_default_services():
    if Service.query.count() == 0:
        default_services = [
            {
                "name": "Birth Certificate",
                "description": "Apply for official birth certificate for identification and documentation.",
                "category": "certificates",
                "icon": "person-badge",
                "fee": 0.0,
                "processing_days": 5,
                "required_documents": "Birth proof, Address proof, ID proof",
                "is_active": True,
            },
            {
                "name": "Income Certificate",
                "description": "Request income verification for welfare schemes and student support.",
                "category": "certificates",
                "icon": "cash-coin",
                "fee": 0.0,
                "processing_days": 7,
                "required_documents": "Income details, ID proof, Address proof",
                "is_active": True,
            },
            {
                "name": "Caste Certificate",
                "description": "Application for caste verification and reservation support.",
                "category": "certificates",
                "icon": "people-fill",
                "fee": 0.0,
                "processing_days": 8,
                "required_documents": "Caste proof, Address proof, ID proof",
                "is_active": True,
            },
            {
                "name": "Marriage Certificate",
                "description": "Get legal confirmation of marriage for documentation and official records.",
                "category": "documents",
                "icon": "heart-fill",
                "fee": 0.0,
                "processing_days": 6,
                "required_documents": "Marriage proof, ID proof, Address proof",
                "is_active": True,
            },
            {
                "name": "Residence Certificate",
                "description": "Proof of residential status for local governance and legal use.",
                "category": "documents",
                "icon": "house-fill",
                "fee": 0.0,
                "processing_days": 4,
                "required_documents": "Address proof, Utility bill, ID proof",
                "is_active": True,
            },
            {
                "name": "Senior Citizen Benefits",
                "description": "Support for elderly citizens including pension and welfare assistance.",
                "category": "welfare",
                "icon": "person-circle",
                "fee": 0.0,
                "processing_days": 10,
                "required_documents": "Age proof, ID proof, Address proof",
                "is_active": True,
            },
        ]
        for item in default_services:
            db.session.add(Service(**item))
        db.session.commit()


@app.context_processor
def inject_context():
    unread_count = 0
    if current_user.is_authenticated:
        unread_count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return {"unread_count": unread_count}


@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
            city=form.city.data,
            pincode=form.pincode.data,
            aadhar_number=form.aadhar_number.data or None,
            role="user",
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Login successful!", "success")
            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))
            if user.role == "staff":
                return redirect(url_for("staff_dashboard"))
            return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))
    if current_user.role == "staff":
        return redirect(url_for("staff_dashboard"))

    services = Service.query.filter_by(is_active=True).all()
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.submitted_at.desc()).limit(5).all()
    pending_count = Application.query.filter_by(user_id=current_user.id, status="pending").count()
    approved_count = Application.query.filter_by(user_id=current_user.id, status="approved").count()
    return render_template(
        "dashboard.html",
        services=services,
        applications=applications,
        pending_count=pending_count,
        approved_count=approved_count,
    )


@app.route("/services")
@login_required
def services():
    services = Service.query.filter_by(is_active=True).all()
    return render_template("services.html", services=services)


@app.route("/service/<int:service_id>", methods=["GET", "POST"])
@login_required
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    if request.method == "POST":
        form_data = {k: v for k, v in request.form.items()}
        app_count = Application.query.count() + 1
        application_number = f"PG{datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y%m%d')}{app_count:04d}"
        application = Application(
            user_id=current_user.id,
            service_id=service.id,
            application_number=application_number,
            status="pending",
            form_data=json.dumps(form_data),
        )
        db.session.add(application)
        db.session.commit()

        notification = Notification(
            user_id=current_user.id,
            title="Application Submitted",
            message=f"Your application for {service.name} has been submitted successfully.",
            notification_type="success",
            is_read=False,
        )
        db.session.add(notification)
        db.session.commit()
        flash(f"Application submitted successfully. Number: {application_number}", "success")
        return redirect(url_for("my_applications"))
    return render_template("service_detail.html", service=service)


@app.route("/my-applications")
@login_required
def my_applications():
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.submitted_at.desc()).all()
    return render_template("my_applications.html", applications=applications)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/admin/dashboard")
@login_required
@role_required("admin")
def admin_dashboard():
    total_users = User.query.count()
    total_services = Service.query.count()
    total_applications = Application.query.count()
    pending_applications = Application.query.filter_by(status="pending").count()
    approved_applications = Application.query.filter_by(status="approved").count()
    recent_applications = Application.query.order_by(Application.submitted_at.desc()).limit(10).all()
    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_services=total_services,
        total_applications=total_applications,
        pending_applications=pending_applications,
        approved_applications=approved_applications,
        recent_applications=recent_applications,
    )


@app.route("/admin/services", methods=["GET", "POST"])
@login_required
@role_required("admin")
def admin_services():
    form = ServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            icon=form.icon.data or "file-earmark",
            fee=float(form.fee.data or 0),
            processing_days=int(form.processing_days.data or 7),
            required_documents=form.required_documents.data,
            is_active=form.is_active.data,
        )
        db.session.add(service)
        db.session.commit()
        flash("Service added successfully.", "success")
        return redirect(url_for("admin_dashboard"))
    services = Service.query.order_by(Service.id.desc()).all()
    return render_template("add_service.html", form=form, services=services)


@app.route("/staff/dashboard")
@login_required
@role_required("staff", "admin")
def staff_dashboard():
    applications = Application.query.order_by(Application.submitted_at.desc()).all()
    total_applications = Application.query.count()
    pending_count = Application.query.filter_by(status="pending").count()
    approved_count = Application.query.filter_by(status="approved").count()
    rejected_count = Application.query.filter_by(status="rejected").count()
    return render_template(
        "staff_dashboard.html",
        applications=applications,
        total_applications=total_applications,
        pending_count=pending_count,
        approved_count=approved_count,
        rejected_count=rejected_count,
    )


@app.route("/staff/application/<int:application_id>", methods=["GET", "POST"])
@login_required
@role_required("staff", "admin")
def review_application(application_id):
    application = Application.query.get_or_404(application_id)
    form = ApplicationReviewForm()
    if form.validate_on_submit():
        application.status = form.status.data
        application.admin_notes = form.approval_notes.data
        application.updated_at = datetime.now(pytz.timezone("Asia/Kolkata"))
        db.session.add(application)
        db.session.commit()
        flash("Application status updated.", "success")
        return redirect(url_for("staff_dashboard"))
    form.status.data = application.status
    form.approval_notes.data = application.admin_notes
    form_data = json.loads(application.form_data) if application.form_data else {}
    return render_template("review_application.html", application=application, form=form, form_data=form_data)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    return render_template("500.html"), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_default_admin()
        create_default_services()
    app.run(debug=True, host="0.0.0.0", port=5000)

