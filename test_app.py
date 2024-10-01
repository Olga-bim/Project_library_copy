import unittest

class TestInitialData(unittest.TestCase):

    def setUp(self):
        from app import app, db, create_initial_data
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        create_initial_data()

    def tearDown(self):
        from app import db
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_customers_exist(self):
        from app import Customer
        self.assertGreater(Customer.query.count(), 0, "Customers not found!")

    def test_books_exist(self):
        from app import Book
        self.assertGreater(Book.query.count(), 0, "Books not found!")

    def test_loans_exist(self):
        from app import Loan
        self.assertGreater(Loan.query.count(), 0, "Loans not found!")

if __name__ == '__main__':
    unittest.main()
