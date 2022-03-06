from flask import Flask, render_template

from models import db

from articles import article
from user import user

from __init__ import celery
from celery_utils import make_celery

def create_flask_app():
    app = Flask(__name__)
    app.config.from_pyfile("configs/default.py")
    db.init_app(app)
        
    app.register_blueprint(article)
    app.register_blueprint(user)

    celery_app = make_celery(celery, app)

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("errors/500.html"), 500

    @app.errorhandler(404)
    def internal_server_error(error):
        return render_template("errors/404.html"), 404

    return app, celery_app