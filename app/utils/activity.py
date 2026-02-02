from flask_login import current_user
from app.extensions import db
from app.models import Activity
from datetime import datetime


def add_activity(action, user=None):
    # Case 1: explicit user passed (registration)
    if user is not None:
        user_id = user.id

    # Case 2: logged-in user
    elif current_user.is_authenticated:
        user_id = current_user.id

    # Case 3: no user context → DO NOTHING
    else:
        return

    activity = Activity(user_id=user_id, action=action, timestamp=datetime.utcnow())

    db.session.add(activity)
    db.session.commit()
