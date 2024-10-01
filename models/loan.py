from datetime import datetime, timedelta
from extensions import db  # Импортируйте db из extensions.py
from enum import Enum



class LoanType(Enum):
    TEN_DAYS = 1
    FIVE_DAYS = 2
    TWO_DAYS = 3

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    def set_return_date(self, duration_days):
        self.return_date = self.loan_date + timedelta(days=duration_days)
