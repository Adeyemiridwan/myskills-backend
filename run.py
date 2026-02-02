# Entry point of the application
# This file is responsible for creating and running the Flask app

from app import create_app, db

# Create the Flask app using the app factory
app = create_app()


with app.app_context():
    db.create_all()

    from app.models import Category

    if Category.query.count() == 0:
        default_categories = [
            "Backend Development",
            "Frontend Development",
            "UI/UX Design",
            "Database",
            "DevOps",
            "Cybersecurity",
            "Artificial Intelligence",
            "Other",
            "Marketing",
            "Finance",
            "Writing",
            "Data",
        ]
        for name in default_categories:
            db.session.add(Category(name=name))
        db.session.commit()


# Run the application in development mode
if __name__ == "__main__":
    app.run(debug=True)
