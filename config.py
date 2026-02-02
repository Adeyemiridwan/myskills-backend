import os


class Config:
    # Base directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-later"

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(BASE_DIR, "myskills.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session & Cookies
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True  # True in production
    SESSION_COOKIE_SAMESITE = "Lax"

    # CSRF
    WTF_CSRF_ENABLED = True
    REMEMBER_COOKIE_SECURE = False
