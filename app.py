from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, timedelta
from models import db, Admin, Student, Book, Borrow, Exam

app = Flask(__name__)
app.secret_key = 'change_this_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    if not Admin.query.filter_by(username='admin').first():
        db.session.add(Admin(username='admin', password='password123'))
        db.session.commit()

def calc_fine(due, ret):
    delta = (ret - due).days
    return 10 * max(0, delta)

# Updated: Standalone, professional admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin'):
        return redirect(url_for('dashboard'))
    error = None
    if request.method == 'POST':
        admin = Admin.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if admin:
            session['admin'] = admin.username
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username or password"
    return render_template('admin_login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    students = Student.query.all()
    books = Book.query.all()
    borrows = Borrow.query.all()
    exams = Exam.query.all()
    return render_template('dashboard.html', students=students, books=books, borrows=borrows, exams=exams)

@app.route('/students', methods=['GET', 'POST'])
def student_list():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        s = Student(id=request.form['id'], name=request.form['name'], email=request.form['email'])
        db.session.add(s)
        db.session.commit()
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/books', methods=['GET', 'POST'])
def books_list():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        b = Book(id=request.form['id'], title=request.form['title'], author=request.form['author'], copies=int(request.form['copies']))
        db.session.add(b)
        db.session.commit()
    books = Book.query.all()
    return render_template('books.html', books=books)

@app.route('/borrow', methods=['POST'])
def borrow_book():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    bid = request.form['bid']
    sid = request.form['sid']
    book = Book.query.get(bid)
    if book and book.copies > 0:
        book.copies -= 1
        borrow = Borrow(sid=sid, bid=bid, borrow_date=datetime.today().date(),
                        due_date=datetime.today().date() + timedelta(days=7))
        db.session.add(borrow)
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/return', methods=['POST'])
def return_book():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    sid = request.form['sid']
    bid = request.form['bid']
    borrow = Borrow.query.filter_by(sid=sid, bid=bid, return_date=None).first()
    if borrow:
        today = datetime.today().date()
        fine = calc_fine(borrow.due_date, today)
        borrow.return_date = today
        borrow.fine = fine
        book = Book.query.get(bid)
        book.copies += 1
        db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/exams', methods=['GET', 'POST'])
def exams_list():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        e = Exam(sid=request.form['sid'], exam=request.form['exam'], score=float(request.form['score']))
        db.session.add(e)
        db.session.commit()
    exams = Exam.query.all()
    return render_template('exams.html', exams=exams)

@app.route('/fines')
def fines_view():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    borrows = Borrow.query.filter(Borrow.fine > 0).all()
    return render_template('fines.html', borrows=borrows)

if __name__ == "__main__":
    app.run(debug=True)
