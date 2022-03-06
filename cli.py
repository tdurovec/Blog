from factory import create_flask_app
from models import db, Users

app, celery_app = create_flask_app()

def init_db(app):
     with app.app_context():
        db.create_all()
        print("Database inicialized")

        default_user = Users(username="admin")
        default_user.set_password("admin")

        db.session.add(default_user)
        db.session.commit()
        
        print("Default user was created")