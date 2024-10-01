from extensions import db  # Импортируйте db из extensions.py
from enum import Enum




class CustomerType(Enum):
    AUTHOR = 1
    READER = 2

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    customer_type = db.Column(db.Integer, nullable=False)
