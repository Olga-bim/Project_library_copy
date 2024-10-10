from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_cors import CORS
import os
import logging
from datetime import datetime, timedelta
from extensions import db  # Импортируйте db из extensions.py
from models.book import Book
from models.customer import Customer, CustomerType
from models.loan import Loan, LoanType
from models.cart import Cart

import unittest

app = Flask(__name__)
app.secret_key = '\xde1\xae\\\xc0\x02\xad\xde\xadT\xbf\xf0\x89L\x0b\x9eq\xff\xa2\x07\xb4h\x02'  
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "library.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print(os.urandom(24))  

db.init_app(app)

# Настройка логирования
file_handler = logging.FileHandler('flask_app.log')
file_handler.setLevel(logging.DEBUG)

# Формат логов с указанием времени выполнения функции
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)


# Добавляем обработчик в логгер Flask
if not app.logger.handlers:
    app.logger.addHandler(file_handler)
app.logger.setLevel(logging.DEBUG)  # Уровень логирования для приложения
# Логгируем время выполнения функции
def log_function_time(function_name):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    app.logger.info(f"Function {function_name} was called at {current_time}")


CORS(app)



class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()  # Создаем базы данных для тестов

        # Запускаем функцию для добавления начальных данных
        self.create_initial_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()  # Удаляем базы данных после тестов
        self.app_context.pop()

    def create_initial_data(self):
        # Добавьте здесь ваш код для начальных данных
        if Book.query.count() == 0:
            books = [
                Book(category='Science Fiction', author='Isaac Asimov', name='Foundation', year_published=1951, loan_type=1),
                Book(category='Classic', author='Leo Tolstoy', name='War and Peace', year_published=1869, loan_type=2),
                Book(category='Mystery', author='Agatha Christie', name='Murder on the Orient Express', year_published=1934, loan_type=3),
                Book(category='Fantasy', author='J.R.R. Tolkien', name='The Hobbit', year_published=1937, loan_type=1),
                Book(category='Non-Fiction', author='Stephen Hawking', name='A Brief History of Time', year_published=1988, loan_type=2),
            ]
            db.session.bulk_save_objects(books)
            db.session.commit()

        if Customer.query.count() == 0:
            customers = [
                Customer(name='Alice', city='New York', age=30, email='alice@example.com', customer_type=1),
                Customer(name='Bob', city='Los Angeles', age=25, email='bob@example.com', customer_type=2),
            ]
            db.session.bulk_save_objects(customers)
            db.session.commit()

def test_initial_data(self):
    books = Book.query.all()
    customers = Customer.query.all()

    self.assertEqual(len(books), 5)  # Проверяем, что 5 книг добавлено
    self.assertEqual(len(customers), 2)  # Проверяем, что 2 клиента добавлено

    self.assertEqual(books[0].author, 'Isaac Asimov')  # Проверяем автора первой книги
    self.assertEqual(customers[0].name, 'Alice')  # Проверяем имя первого клиента


def create_tables():
    db.create_all()


def create_initial_data():
    with app.app_context():
        if Book.query.count() == 0:
                    books = [
                Book(category='Science Fiction', author='Isaac Asimov', name='Foundation', year_published=1951, loan_type=1, added_date=datetime(2024, 10, 29)),
                Book(category='Classic', author='Leo Tolstoy', name='War and Peace', year_published=1869, loan_type=2, added_date=datetime(2024, 10, 29)),
                Book(category='Mystery', author='Agatha Christie', name='Murder on the Orient Express', year_published=1934, loan_type=3, added_date=datetime(2024, 10, 29)),
                Book(category='Fantasy', author='J.R.R. Tolkien', name='The Hobbit', year_published=1937, loan_type=1, added_date=datetime(2024, 10, 29)),
                Book(category='Non-Fiction', author='Stephen Hawking', name='A Brief History of Time', year_published=1988, loan_type=2, added_date=datetime(2024, 10, 29)),
            ]
                    db.session.bulk_save_objects(books)
                    db.session.commit()
        else:
            default_books = [
                ('Science Fiction', 'Isaac Asimov', 'Foundation', 1951, 1),
                ('Classic', 'Leo Tolstoy', 'War and Peace', 1869, 2),
                ('Mystery', 'Agatha Christie', 'Murder on the Orient Express', 1934, 3),
                ('Fantasy', 'J.R.R. Tolkien', 'The Hobbit', 1937, 1),
                ('Non-Fiction', 'Stephen Hawking', 'A Brief History of Time', 1988, 2),
            ]
            for category, author, name, year, loan_type in default_books:
                if not Book.query.filter_by(name=name).first():
                    new_book = Book(category=category, author=author, name=name, year_published=year, loan_type=loan_type, added_date=datetime.utcnow())
                    db.session.add(new_book)

            db.session.commit()

        if Customer.query.count() == 0:
            customers = [
                Customer(name='Alice', city='New York', age=30, email='alice@example.com', customer_type=CustomerType.READER.value),
                Customer(name='Bob', city='Los Angeles', age=25, email='bob@example.com', customer_type=CustomerType.AUTHOR.value),
                Customer(name='Charlie', city='Chicago', age=35, email='charlie@example.com', customer_type=CustomerType.READER.value),
                Customer(name='Diana', city='Houston', age=28, email='diana@example.com', customer_type=CustomerType.AUTHOR.value),
                Customer(name='Eve', city='Philadelphia', age=22, email='eve@example.com', customer_type=CustomerType.READER.value),
            ]
            db.session.bulk_save_objects(customers)
            db.session.commit()

        if Loan.query.count() == 0:
            loans = [
                Loan(cust_id=1, book_id=1, loan_date=datetime(2023, 1, 1), return_date=datetime(2023, 1, 11)),
                Loan(cust_id=2, book_id=2, loan_date=datetime(2023, 1, 2), return_date=datetime(2023, 1, 7)),
                Loan(cust_id=3, book_id=3, loan_date=datetime(2023, 1, 3), return_date=datetime(2023, 1, 5)),
                Loan(cust_id=4, book_id=4, loan_date=datetime(2023, 1, 4), return_date=datetime(2023, 1, 14)),
                Loan(cust_id=5, book_id=5, loan_date=datetime(2023, 1, 5), return_date=datetime(2023, 1, 10)),
            ]
            db.session.bulk_save_objects(loans)
            db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/about_website')
def about_website():
    return render_template('about_website.html')

@app.route('/author_books')
def author_books():
    return render_template('author_books.html')


@app.route('/about_website_creator')
def about_website_creator():
    return render_template('about_website_creator.html')


@app.route('/your_route')
def your_view_function():
    books = Book.query.all()  
    loans = Loan.query.all()  

    return render_template('your_template.html', books=books, loans=loans)

@app.route('/customers')
def list_customers():
    customers = Customer.query.all()
    return render_template('list_customers.html', customers=customers)


# CRUD for Customers
@app.route('/admin')
def admin():
    app.logger.info('Accessed admin page')
    customers = Customer.query.all()
    loans = Loan.query.all()  # Retrieve all loans
    books = Book.query.all()  # Retrieve all books
    return render_template('admin.html', customers=customers, loans=loans, books=books, CustomerType=CustomerType)

@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    app.logger.info('add_customer called')
    
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        age = int(request.form['age'])
        email = request.form['email']
        customer_type = int(request.form['customer_type'])

        if Customer.query.filter_by(email=email).first():
            app.logger.warning(f'Email already exists: {email}')
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_customer'))

        new_customer = Customer(
            name=name,
            city=city,
            age=age,
            email=email,
            customer_type=customer_type
        )

        try:
            db.session.add(new_customer)
            db.session.commit()
            app.logger.info(f'New customer added: {new_customer.id}')
            flash('Customer added successfully!')
            return redirect(url_for('admin'))
        except Exception as e:
            db.session.rollback()  # Отменяем изменения в случае ошибки
            app.logger.error(f'Error adding customer: {e}')
            flash('There was an error adding the customer. Please try again.', 'danger')

    return render_template('add_customer.html', CustomerType=CustomerType)



@app.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    app.logger.info(f'edit_customer called for customer id: {id}')
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        customer.name = request.form['name']
        customer.city = request.form['city']
        customer.age = int(request.form['age'])
        customer.email = request.form['email']
        customer.customer_type = int(request.form['customer_type'])
        db.session.commit()
        app.logger.info(f'Customer updated: {customer.id}')
        flash('Customer updated successfully!')
        return redirect(url_for('admin'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/customers/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    app.logger.info(f'Attempting to delete customer id: {id}')
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    flash('Customer deleted successfully!')
    return redirect(url_for('admin'))

# CRUD for Books

@app.route('/books', methods=['GET'])
def list_books():
    app.logger.info('list_books called')
    query = Book.query
    cart_items = Cart.query.filter_by(cust_id=1).all()  

    if 'search_category' in request.args:
        category = request.args.get('category')
        if category:
            query = query.filter(Book.category.ilike(f'%{category}%'))
            app.logger.info(f'Searching books by category: {category}')
    
    if 'search_author' in request.args:
        author = request.args.get('author')
        if author:
            query = query.filter(Book.author.ilike(f'%{author}%'))
            app.logger.info(f'Searching books by author: {author}')
    
    if 'search_year' in request.args:
        year_published = request.args.get('year_published')
        if year_published:
            query = query.filter(Book.year_published == year_published)
            app.logger.info(f'Searching books by year: {year_published}')
    
    if 'show_all' in request.args:
        books = Book.query.all() 
        app.logger.info('Showing all books')
    else:
        books = query.all()

    categories = db.session.query(Book.category).distinct().all()
    authors = db.session.query(Book.author).distinct().all()
    years = db.session.query(Book.year_published).distinct().all()
    delete_success = request.args.get('delete_success', False)
    return render_template('books.html', books=books, cart_items=cart_items, categories=categories, authors=authors, years=years, delete_success=delete_success)




@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    app.logger.info('add_book called')
    if request.method == 'POST':
        category = request.form['category']
        author = request.form['author']
        name = request.form['name']
        year_published = request.form['year_published']
        loan_type = request.form['loan_type']
        
        new_book = Book(category=category, author=author, name=name, year_published=year_published, loan_type=loan_type)
        db.session.add(new_book)
        db.session.commit()
        app.logger.info(f'New book added: {new_book.name} by {new_book.author}')
        return redirect(url_for('list_books'))
    
    return render_template('admin.html')

@app.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    app.logger.info(f'edit_book called for book id: {book_id}')
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        book.category = request.form['category']
        book.author = request.form['author']
        book.name = request.form['name']
        book.year_published = request.form['year_published']
        book.loan_type = request.form['loan_type']
        db.session.commit()
        app.logger.info(f'Book updated: {book.name} by {book.author}')
        flash('Book updated successfully!')
        return redirect(url_for('list_books'))
    return render_template('edit_book.html', book=book)

@app.route('/books/delete/<int:book_id>', methods=['POST']) 
def delete_book(book_id):
    app.logger.info(f'delete_book called for book id: {book_id}')
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    app.logger.info(f'Book deleted: {book.name} by {book.author}')
    flash('Book deleted successfully!')
    return redirect(url_for('list_books', delete_success=True))

# CRUD  для Loans
@app.route('/loans')
def list_loans():
    loans = Loan.query.all()
    app.logger.info(f'Loans retrieved: {loans}')
    return render_template('loans.html', loans=loans)

@app.route('/loans/add', methods=['GET', 'POST'])
def add_loan():
    if request.method == 'POST':
        new_loan = Loan(
            cust_id=request.form['cust_id'],
            book_id=request.form['book_id'],
            loan_date=datetime.strptime(request.form['loan_date'], '%Y-%m-%d')
        )
        
        book = Book.query.get_or_404(new_loan.book_id)
        loan_type = LoanType(book.loan_type)  # Получаем тип займа как Enum

        new_loan.set_return_date(loan_type)  # Устанавливаем дату возврата

        db.session.add(new_loan)
        db.session.commit()
        flash('Loan added successfully!')
        return redirect(url_for('list_loans'))
    
    customers = Customer.query.all()
    books = Book.query.all()  # Получаем список книг
    return render_template('add_loan.html', customers=customers, books=books)


@app.route('/loan_type/<int:book_id>', methods=['GET'])
def get_loan_type(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify(book.loan_type)



@app.route('/loans/edit/<int:id>', methods=['GET', 'POST'])
def edit_loan(id):
    loan = Loan.query.get_or_404(id)
    if request.method == 'POST':
        loan.cust_id = request.form['cust_id']
        loan.book_id = request.form['book_id']
        loan.loan_date = datetime.strptime(request.form['loan_date'], '%Y-%m-%d')
        loan.return_date = datetime.strptime(request.form['return_date'], '%Y-%m-%d')
        db.session.commit()
        flash('Loan updated successfully!')
        return redirect(url_for('list_loans'))
    return render_template('edit_loan.html', loan=loan)

@app.route('/loans/delete/<int:id>', methods=['POST'])
def delete_loan(id):
    loan = Loan.query.get_or_404(id)
    db.session.delete(loan)
    db.session.commit()
    flash('Loan deleted successfully!')
    return redirect(url_for('admin'))  # Redirect to admin page


# CRUD for author books
def get_current_user_id():
    return session.get('user_id')  # Получаем user_id из сессии

def get_categories():
    return ['Fiction', 'Non-Fiction', 'Science', 'History']  # Статический список

def get_loan_types():
    return ['Short-Term', 'Long-Term']  # Статический список

@app.route('/author/books', methods=['GET'])
def list_author_books():
    author_id = get_current_user_id()  
    app.logger.info(f'Listing books for author ID {author_id}')
    books = Book.query.filter_by(author_id=author_id).all()
    return render_template('author_books.html', books=books)

def get_loan_types():
    return {type.name: type.value for type in LoanType}


@app.route('/author/books/add', methods=['GET', 'POST'])
def add_author_book():
    if request.method == 'POST':
        try:
            category = request.form['category']
            author_name = request.form['author']
            name = request.form['name']
            year_published = request.form['year_published']
            loan_type = request.form['loan_type']

            new_book = Book(
                category=category,
                author=author_name,
                name=name,
                year_published=year_published,
                loan_type=loan_type
            )
            db.session.add(new_book)
            db.session.commit()
            flash('The book has been added successfully!')
            app.logger.info(f'Book "{name}" added successfully for author "{author_name}".')
            return redirect(url_for('list_books'))
        except Exception as e:
            app.logger.error(f'Error adding book: {str(e)}')
            flash('An error occurred while adding the book. Please try again.')

    return render_template('add_author_book.html', categories=get_categories(), loan_types=get_loan_types())


@app.route('/author/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_author_book(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == 'POST':
        book.category = request.form['category']
        book.author = request.form['author']
        book.name = request.form['name']
        book.year_published = request.form['year_published']
        book.loan_type = request.form['loan_type']
        db.session.commit()
        flash('Book updated successfully!')
        app.logger.info(f'Book ID {book_id} updated successfully.')
        return redirect(url_for('list_books'))

    return render_template('edit_author_book.html', book=book)

@app.route('/author/delete_book/<int:book_id>', methods=['POST'])
def delete_author_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!')
    app.logger.info(f'Book ID {book_id} deleted successfully.')
    return redirect(url_for('list_books'))


if __name__ == '__main__':
    with app.app_context():
        create_tables()  
        create_initial_data()  
    app.run(debug=True)