from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.extensions import db, bcrypt
from app.models import User
from app.forms import LoginForm, RegistrationForm
from app.utils.activity import add_activity


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for("profile.dashboard"))

    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken", "danger")
            return redirect(url_for("auth.register"))

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )

        db.session.add(new_user)
        db.session.commit()
        add_activity(action="Registered Account", user=new_user)

        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        identifier = form.identifier.data

        if "@" in identifier:
            user = User.query.filter_by(email=identifier).first()
        else:
            user = User.query.filter_by(username=identifier).first()

        # ❌ User not found
        if not user:
            flash("Account not found", "danger")
            return redirect(url_for("auth.login"))

        # ❌ Wrong password
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash("Incorrect password", "danger")
            return redirect(url_for("auth.login"))

        # ✅ Success
        login_user(user)

        previous_login = user.current_login
        user.last_login = previous_login
        user.current_login = datetime.utcnow()
        db.session.commit()

        add_activity("Logged in")

        flash("Logged in successfully", "success")
        return redirect(url_for("profile.dashboard"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    # Track logout activity BEFORE logging out
    add_activity("Logged out")
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))
