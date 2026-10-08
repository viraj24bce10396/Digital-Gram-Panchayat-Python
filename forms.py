from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, Regexp


class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired(), Regexp(r"^\+?\d{10,15}$")])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=10, max=500)])
    city = StringField("City", validators=[DataRequired(), Length(min=2, max=60)])
    pincode = StringField("Pincode", validators=[DataRequired(), Regexp(r"^\d{6}$")])
    aadhar_number = StringField("Aadhar Number (optional)", validators=[Optional(), Regexp(r"^\d{12}$")])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateProfileForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired(), Regexp(r"^\+?\d{10,15}$")])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=10, max=500)])
    city = StringField("City", validators=[DataRequired(), Length(min=2, max=60)])
    pincode = StringField("Pincode", validators=[DataRequired(), Regexp(r"^\d{6}$")])
    submit = SubmitField("Update Profile")


class ServiceForm(FlaskForm):
    name = StringField("Service Name", validators=[DataRequired(), Length(min=3, max=120)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(min=10, max=1000)])
    category = SelectField(
        "Category",
        choices=[
            ("certificates", "Certificates"),
            ("documents", "Documents"),
            ("welfare", "Welfare Services"),
            ("other", "Other Services"),
        ],
        validators=[DataRequired()],
    )
    icon = StringField("Icon Name", validators=[Optional()])
    fee = FloatField("Fee (₹)", validators=[Optional()])
    processing_days = IntegerField("Processing Days", validators=[Optional()])
    required_documents = TextAreaField("Required Documents", validators=[Optional()])
    is_active = BooleanField("Active")
    submit = SubmitField("Save Service")


class ApplicationReviewForm(FlaskForm):
    status = SelectField(
        "Status",
        choices=[
            ("pending", "Pending"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
            ("completed", "Completed"),
        ],
        validators=[DataRequired()],
    )
    approval_notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Update Status")
