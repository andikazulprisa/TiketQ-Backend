from flask import Flask
from app.db import db

def create_app():
    
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        from app.routes import ticket_routes
        app.register_blueprint(ticket_routes)
        db.create_all()

    return app
