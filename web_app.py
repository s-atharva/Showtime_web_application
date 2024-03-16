from flask import Flask, session, g
from services.user import user_services
from services.theatre import theatre_services


def add_routes(app: Flask):
    @app.before_request
    def before_request():
        g.user_name = None
        g.is_admin = None
        g.user_id = None
        if "user_name" in session and "is_admin" in session and "user_id" in session:
            g.user_name = session["user_name"]
            g.is_admin = session["is_admin"]
            g.user_id = session["user_id"]


def register_blueprints(app: Flask):
    app.register_blueprint(user_services)
    app.register_blueprint(theatre_services)


def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "your_secret_key"
    add_routes(app=app)
    register_blueprints(app=app)
    return app
