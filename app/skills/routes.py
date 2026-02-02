from flask import Blueprint, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.extensions import db
from app.models import Skill, Category, User
from app.forms import SkillForm, DeleteForm
from app.utils.activity import add_activity


skills_bp = Blueprint("skills", __name__, url_prefix="/skills")

# ==========================
# Add Skill
# ==========================


@skills_bp.route("/")
@login_required
def skills():
    skills = Skill.query.filter_by(user_id=current_user.id).all()
    delete_form = DeleteForm()
    return render_template("skills/skills.html", skills=skills, delete_form=delete_form)


@skills_bp.route("/add-skill", methods=["GET", "POST"])
@login_required
def add_skill():
    form = SkillForm()

    # Load categories for dropdown
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    # Skill limit check
    skill_count = Skill.query.filter_by(user_id=current_user.id).count()
    if skill_count >= 20:
        flash("Skill limit reached. Remove a skill to add another.", "info")
        return redirect(url_for("skills.skills"))

    if form.validate_on_submit():
        # Check category
        category = Category.query.get(form.category_id.data)
        if not category:
            flash("Invalid category selected.", "danger")
            return redirect(url_for("skills.add_skill"))

        # Prevent duplicates
        existing_skill = Skill.query.filter_by(
            user_id=current_user.id, title=form.title.data.strip()
        ).first()

        if existing_skill:
            flash("You already added this skill.", "warning")
            return redirect(url_for("skills.add_skill"))

        # Save skill
        new_skill = Skill(
            title=form.title.data,
            level=form.level.data,
            description=form.description.data,
            category_id=form.category_id.data,
            user_id=current_user.id,
        )

        db.session.add(new_skill)
        db.session.commit()

        add_activity(action=f"Added skill: {new_skill.title}")

        flash("Skill added successfully", "success")
        return redirect(url_for("profile.dashboard"))

    return render_template("skills/add_skill.html", form=form)


@skills_bp.route("/skills/<int:skill_id>/edit", methods=["GET", "POST"])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)

    # Security check
    if skill.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for("profile.dashboard"))

    form = SkillForm(obj=skill)

    # Load Category Choices
    form.category_id.choices = [
        (c.id, c.name) for c in Category.query.order_by(Category.name).all()
    ]

    if form.validate_on_submit():
        skill.title = form.title.data
        skill.level = form.level.data
        skill.description = form.description.data
        skill.category_id = form.category_id.data

        db.session.commit()
        add_activity(action=f"Updated skill: {skill.title}")
        flash("Skill updated successfully", "success")
        return redirect(url_for("profile.dashboard"))

    # Prefill Form On First Load
    form.title.data = skill.title
    form.level.data = skill.level
    form.description.data = skill.description
    form.category_id.data = skill.category_id

    return render_template("skills/edit_skill.html", form=form)


@skills_bp.route("/skills/<int:skill_id>/delete", methods=["POST"])
@login_required
def delete_skill(skill_id):
    form = DeleteForm()

    if not form.validate_on_submit():
        abort(400)

    skill = Skill.query.get_or_404(skill_id)

    if skill.user_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect(url_for("profile.dashboard"))

    db.session.delete(skill)
    db.session.commit()

    add_activity(action=f"Deleted skill: {skill.title}")
    flash("Skill deleted", "success")
    return redirect(url_for("profile.dashboard"))
