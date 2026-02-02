from flask import Flask
from config import Config
from app.extensions import db, bcrypt, login_manager, csrf


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.profile.routes import profile_bp
    from app.skills.routes import skills_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(skills_bp, url_prefix="/skills")

    return app


from app.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
