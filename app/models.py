from app.db import db
from datetime import datetime

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    isUsed = db.Column(db.Boolean, default=False)