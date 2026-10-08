"""
Digital Gram Panchayat - Automated Unit & Integration Tests
Tests authentication mechanisms, database models, route protections,
and form validations using Python's standard unittest runner.
"""

import unittest
from app import app
from models import db, User, Service, Application


class DigitalGramPanchayatTestCase(unittest.TestCase):
    def setUp(self):
        """Set up in-memory SQLite database and test client."""
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Clean up database session and drop tables."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_password_hashing(self):
        """Test password hashing and verification."""
        user = User(
            full_name="Test Citizen",
            email="citizen@example.com",
            phone="9876543210",
            role="user",
            address="Ward 4",
            city="Sample Village",
            pincode="123456",
        )
        user.set_password("SecurePassword123")
        self.assertNotEqual(user.password_hash, "SecurePassword123")
        self.assertTrue(user.check_password("SecurePassword123"))
        self.assertFalse(user.check_password("WrongPassword"))

    def test_public_home_route(self):
        """Test home page returns 200 OK."""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

    def test_public_services_route(self):
        """Test services catalog route returns 200 OK."""
        response = self.app.get("/services")
        self.assertEqual(response.status_code, 200)

    def test_login_route_accessible(self):
        """Test login page loads successfully."""
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_register_route_accessible(self):
        """Test registration page loads successfully."""
        response = self.app.get("/register")
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_dashboard_redirect(self):
        """Test that unauthenticated requests to protected dashboard redirect to login."""
        response = self.app.get("/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_unauthenticated_admin_redirect(self):
        """Test that unauthenticated access to admin dashboard redirects to login."""
        response = self.app.get("/admin/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])

    def test_unauthenticated_staff_redirect(self):
        """Test that unauthenticated access to staff dashboard redirects to login."""
        response = self.app.get("/staff/dashboard", follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.headers["Location"])


if __name__ == "__main__":
    unittest.main()
