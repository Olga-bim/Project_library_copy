from datetime import datetime, timedelta
from extensions import db  # Импортируйте db из extensions.py
from enum import Enum

# Перечисление для сроков займа книг
class LoanType(Enum):
    TEN_DAYS = 10  # 10 дней
    FIVE_DAYS = 5  # 5 дней
    TWO_DAYS = 2   # 2 дня

# Модель Loan для управления займами книг
class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    # Метод для установки даты возврата на основе длительности займа
    def set_return_date(self, loan_type):
        # loan_type должен быть объектом LoanType Enum
        self.return_date = self.loan_date + timedelta(days=loan_type.value)
