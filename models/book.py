from datetime import datetime, timedelta
from extensions import db  # Импортируйте db из extensions.py
from enum import Enum



class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    loan_type = db.Column(db.Integer, nullable=False)
    added_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
