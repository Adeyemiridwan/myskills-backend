from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# ==========================
# Authentication For Registration Forms
# ==========================


class RegistrationForm(FlaskForm):
    """
    Form used to register new users.
    """

    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords do not match"),
        ],
    )
    submit = SubmitField("Register")


# ==========================
# Authentication For Login Forms
# ==========================


class LoginForm(FlaskForm):
    """
    Form used to log in existing users using either username or email.
    """

    identifier = StringField("Username or Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


# ==========================
# Update Profile Forms
# ==========================


class UpdateProfileForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update Profile")


# ==========================
# Update Password Forms
# ==========================


class changePasswordForm(FlaskForm):
    current_password = PasswordField("Current Password", validators=[DataRequired()])
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=6)]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            Length(min=6),
            EqualTo("new_password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Update Password")


# ==========================
# Skill Form
# ==========================


class SkillForm(FlaskForm):
    title = StringField(
        "Skill Title",
        validators=[
            DataRequired(message="Skill name is required."),
            Length(min=2, max=50),
        ],
    )

    level = SelectField(
        "Skill Level",
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
            ("Expert", "Expert"),
        ],
        validators=[DataRequired()],
    )

    description = TextAreaField("Description", validators=[Length(max=500)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])

    submit = SubmitField("Add Skill")


# ==========================
# Delete Form
# ==========================
class DeleteForm(FlaskForm):
    pass
