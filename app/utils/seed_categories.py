from app.extensions import db
from app.models import Category


DEFAULT_CATEGORIES = [
    "Backend Development",
    "Frontend Development",
    "UI/UX Design",
    "Database",
    "DevOps",
    "Cybersecurity",
    "Artificial Intelligence",
    "Other",
]


def seed_categories():
    # Check if categories already exist
    if Category.query.first():
        return  # Already seeded

    for name in DEFAULT_CATEGORIES:
        category = Category(name=name)
        db.session.add(category)

    db.session.commit()
