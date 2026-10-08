"""
Digital Gram Panchayat - Management CLI Utility
Provides administrative and operational CLI commands for database management,
user administration, system diagnostics, and reporting.

Usage:
    python manage.py <command> [options]

Commands:
    init-db        Initialize the SQLite database and seed initial admin & services
    create-user    Provision a new user (admin, staff, or user)
    list-users     Display all registered accounts and roles
    list-services  Display the public civic services catalog
    stats          Display platform overview statistics
    health-check   Run basic diagnostics on database and configurations
"""

import argparse
import sys

try:
    from app import app, create_default_admin, create_default_services
    from models import Application, AuditLog, Notification, Service, User, db
except ImportError as e:
    print(f"Error importing application modules: {e}")
    print("Please ensure dependencies are installed (pip install -r requirements.txt).")
    sys.exit(1)


def init_db():
    """Initializes database tables and seeds default records."""
    with app.app_context():
        db.create_all()
        create_default_admin()
        create_default_services()
        print("[SUCCESS] Database tables created and seed data initialized.")


def create_user(
    full_name,
    email,
    password,
    role="user",
    phone="0000000000",
    address="Local",
    city="Village",
    pincode="000000",
):
    """Provisions a new user account with specified role."""
    with app.app_context():
        existing = User.query.filter_by(email=email).first()
        if existing:
            print(f"[ERROR] User with email '{email}' already exists.")
            return

        new_user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            role=role,
            address=address,
            city=city,
            pincode=pincode,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        print(f"[SUCCESS] User '{full_name}' ({email}) created with role '{role}'.")


def list_users():
    """Lists all registered users in the database."""
    with app.app_context():
        users = User.query.all()
        if not users:
            print("[INFO] No users found in database.")
            return

        print(f"\n{'ID':<5} {'Role':<10} {'Name':<25} {'Email':<30} {'Phone':<15}")
        print("-" * 85)
        for u in users:
            print(f"{u.id:<5} {u.role:<10} {u.full_name:<25} {u.email:<30} {u.phone:<15}")
        print(f"\nTotal users: {len(users)}\n")


def list_services():
    """Lists all public services in the catalog."""
    with app.app_context():
        services = Service.query.all()
        if not services:
            print("[INFO] No services registered.")
            return

        print(f"\n{'ID':<5} {'Category':<15} {'Name':<28} {'Fee':<10} {'Days':<6} {'Active':<8}")
        print("-" * 75)
        for s in services:
            print(
                f"{s.id:<5} {s.category:<15} {s.name:<28} Rs.{s.fee:<8.2f} {s.processing_days:<6} {str(s.is_active):<8}"
            )
        print(f"\nTotal services: {len(services)}\n")


def print_stats():
    """Prints system usage metrics and application counters."""
    with app.app_context():
        total_users = User.query.count()
        total_citizens = User.query.filter_by(role="user").count()
        total_staff = User.query.filter_by(role="staff").count()
        total_admins = User.query.filter_by(role="admin").count()

        total_apps = Application.query.count()
        pending_apps = Application.query.filter_by(status="pending").count()
        approved_apps = Application.query.filter_by(status="approved").count()
        rejected_apps = Application.query.filter_by(status="rejected").count()
        total_services = Service.query.count()

        print("\n================ Digital Gram Panchayat Statistics ================")
        print(f" Total Registered Accounts : {total_users}")
        print(f"   |-- Citizens             : {total_citizens}")
        print(f"   |-- Staff Members        : {total_staff}")
        print(f"   \\-- Administrators       : {total_admins}")
        print(f" Active Public Services    : {total_services}")
        print(f" Total Service Requests    : {total_apps}")
        print(f"   |-- Pending Review       : {pending_apps}")
        print(f"   |-- Approved             : {approved_apps}")
        print(f"   \\-- Rejected             : {rejected_apps}")
        print("===================================================================\n")


def health_check():
    """Performs environment and database connection diagnostics."""
    print("\nRunning Digital Gram Panchayat diagnostics...")
    with app.app_context():
        try:
            db.engine.connect()
            print("[OK] Database connection established.")
        except Exception as err:
            print(f"[FAIL] Database connection error: {err}")
            return

        admin = User.query.filter_by(role="admin").first()
        if admin:
            print(f"[OK] Administrative account verified ({admin.email}).")
        else:
            print("[WARN] No administrator account found. Run 'python manage.py init-db'.")

        services_count = Service.query.count()
        print(f"[OK] {services_count} civic service(s) configured.")
        print("[SUCCESS] Diagnostics passed.\n")


def main():
    parser = argparse.ArgumentParser(description="Digital Gram Panchayat Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init-db
    subparsers.add_parser("init-db", help="Initialize database tables and seed defaults")

    # create-user
    create_parser = subparsers.add_parser("create-user", help="Create a new user")
    create_parser.add_argument("--name", required=True, help="Full name")
    create_parser.add_argument("--email", required=True, help="Email address")
    create_parser.add_argument("--password", required=True, help="User password")
    create_parser.add_argument(
        "--role", default="user", choices=["admin", "staff", "user"], help="User role"
    )
    create_parser.add_argument("--phone", default="0000000000", help="Phone number")
    create_parser.add_argument("--address", default="Village Area", help="Address")
    create_parser.add_argument("--city", default="Gram Panchayat", help="City / Village")
    create_parser.add_argument("--pincode", default="123456", help="Pincode")

    # list-users
    subparsers.add_parser("list-users", help="List all users")

    # list-services
    subparsers.add_parser("list-services", help="List all services")

    # stats
    subparsers.add_parser("stats", help="Display platform statistics")

    # health-check
    subparsers.add_parser("health-check", help="Run system diagnostics")

    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
    elif args.command == "create-user":
        create_user(
            args.name,
            args.email,
            args.password,
            args.role,
            args.phone,
            args.address,
            args.city,
            args.pincode,
        )
    elif args.command == "list-users":
        list_users()
    elif args.command == "list-services":
        list_services()
    elif args.command == "stats":
        print_stats()
    elif args.command == "health-check":
        health_check()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
