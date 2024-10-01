from datetime import datetime, timedelta
from extensions import db  # Импортируйте db из extensions.py
from enum import Enum




class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)
    added_by_author = db.Column(db.Boolean, nullable=False, default=False)

    customer = db.relationship('Customer', backref='carts')
    book = db.relationship('Book', backref='carts')
