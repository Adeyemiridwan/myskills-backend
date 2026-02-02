from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.extensions import db, bcrypt
from app.models import Activity, User, Skill
from app.forms import UpdateProfileForm, changePasswordForm
from app.utils.activity import add_activity


profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/dashboard")
@login_required
def dashboard():
    total_skills = Skill.query.filter_by(user_id=current_user.id).count()

    last_skill = (
        Skill.query.filter_by(user_id=current_user.id)
        .order_by(Skill.created_at.desc())
        .first()
    )

    activity_list = (
        Activity.query.filter_by(user_id=current_user.id)
        .order_by(Activity.timestamp.desc())
        .limit(5)
        .all()
    )

    return render_template(
        "profile/dashboard.html",
        user=current_user,
        total_skills=total_skills,
        last_skill=last_skill,
        activities=activity_list,
    )


@profile_bp.route("/activities")
@login_required
def activities():
    activity_list = (
        Activity.query.filter_by(user_id=current_user.id)
        .order_by(Activity.timestamp.desc())
        .all()
    )

    return render_template("profile/activities.html", activities=activity_list)


@profile_bp.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    form = UpdateProfileForm()

    if form.validate_on_submit():
        # Check username
        existing_username = User.query.filter(
            User.username == form.username.data, User.id != current_user.id
        ).first()

        if existing_username:
            flash("Username already taken", "danger")
            return redirect(url_for("profile.update_profile"))

        # Check email
        existing_email = User.query.filter(
            User.email == form.email.data, User.id != current_user.id
        ).first()

        if existing_email:
            flash("Email already in use", "danger")
            return redirect(url_for("profile.update_profile"))

        # Update safely
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        add_activity(action=f"Profile Updated")

        flash("Profile updated successfully", "success")
        return redirect(url_for("profile.dashboard"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("profile/update_profile.html", form=form)


@profile_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = changePasswordForm()

    if form.validate_on_submit():

        # 1️⃣ Verify current password
        if not bcrypt.check_password_hash(
            current_user.password, form.current_password.data
        ):
            flash("Current password is incorrect", "danger")
            return redirect(url_for("profile.change_password"))

        # 2️⃣ WTForms already checks password match
        # (EqualTo validator does this)

        # 3️⃣ Save new password ONLY if all checks passed
        current_user.password = bcrypt.generate_password_hash(
            form.new_password.data
        ).decode("utf-8")

        db.session.commit()

        add_activity("Changed Password")

        flash("Password changed successfully", "success")
        return redirect(url_for("profile.dashboard"))

    return render_template("profile/change_password.html", form=form)
