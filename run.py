# Entry point of the application
# This file is responsible for creating and running the Flask app

from app import create_app, db

# Create the Flask app using the app factory
app = create_app()

from app.models import Category

with app.app_context():
    db.create_all()

    if Category.query.count() == 0:
        from app.utils.seed import seed_categories

        seed_categories()


# Run the application in development mode
if __name__ == "__main__":
    app.run(debug=True)
