from flask import Blueprint, render_template

# ==========================
# Blueprint Setup
# ==========================

main_bp = Blueprint("main", __name__)

# ==========================
# Public Routes
# ==========================

@main_bp.route("/")
def home():
    return render_template("main/home.html")
