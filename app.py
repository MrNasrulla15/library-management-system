from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
from openpyxl import load_workbook, Workbook
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_in_production'

# File paths
BOOKS_FILE = 'data/books.xlsx'
ISSUED_FILE = 'data/issued_books.xlsx'
STUDENTS_FILE = 'data/students.xlsx'
LIBRARIAN_CREDS = {'username': 'admin', 'password': 'admin123'}

# Initialize Excel files if they don't exist
def init_files():
    os.makedirs('data', exist_ok=True)
    
    # Initialize books file
    if not os.path.exists(BOOKS_FILE):
        df = pd.DataFrame(columns=['Book_ID', 'Title', 'Author', 'Total_Copies', 'Available_Copies'])
        # Add some sample books
        sample_books = [
            ['B001', 'To Kill a Mockingbird', 'Harper Lee', 3, 3],
            ['B002', '1984', 'George Orwell', 2, 2],
            ['B003', 'The Great Gatsby', 'F. Scott Fitzgerald', 4, 4],
            ['B004', 'Pride and Prejudice', 'Jane Austen', 2, 2],
            ['B005', 'Harry Potter and the Sorcerer\'s Stone', 'J.K. Rowling', 5, 5]
        ]
        df = pd.DataFrame(sample_books, columns=['Book_ID', 'Title', 'Author', 'Total_Copies', 'Available_Copies'])
        df.to_excel(BOOKS_FILE, index=False)
    
    # Initialize issued books file
    if not os.path.exists(ISSUED_FILE):
        df = pd.DataFrame(columns=['Book_ID', 'Title', 'Student_Name', 'Student_ID', 'Issue_Date', 'Return_Date'])
        df.to_excel(ISSUED_FILE, index=False)
    
    # Initialize students file
    if not os.path.exists(STUDENTS_FILE):
        df = pd.DataFrame(columns=['Student_ID', 'Name', 'Email', 'Password', 'Phone', 'Registration_Date'])
        # Add a sample student (password: student123)
        hashed_password = generate_password_hash('student123')
        sample_student = [['STU001', 'John Doe', 'john@example.com', hashed_password, '1234567890', datetime.now().strftime('%Y-%m-%d')]]
        df = pd.DataFrame(sample_student, columns=['Student_ID', 'Name', 'Email', 'Password', 'Phone', 'Registration_Date'])
        df.to_excel(STUDENTS_FILE, index=False)

init_files()

# Helper functions
def read_books():
    return pd.read_excel(BOOKS_FILE)

def write_books(df):
    df.to_excel(BOOKS_FILE, index=False)

def read_issued():
    return pd.read_excel(ISSUED_FILE)

def write_issued(df):
    df.to_excel(ISSUED_FILE, index=False)

def read_students():
    return pd.read_excel(STUDENTS_FILE)

def write_students(df):
    df.to_excel(STUDENTS_FILE, index=False)

def generate_student_id():
    df = read_students()
    if len(df) == 0:
        return 'STU001'
    last_id = df['Student_ID'].iloc[-1]
    num = int(last_id[3:]) + 1
    return f'STU{num:03d}'

# Routes
@app.route('/')
def home():
    return render_template('home.html')

# Student Routes
@app.route('/student/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        
        students_df = read_students()
        
        # Check if email already exists
        if email in students_df['Email'].values:
            flash('Email already registered! Please login.', 'error')
            return redirect(url_for('student_login'))
        
        # Generate student ID
        student_id = generate_student_id()
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Add new student
        registration_date = datetime.now().strftime('%Y-%m-%d')
        new_student = pd.DataFrame([[student_id, name, email, hashed_password, phone, registration_date]], 
                                   columns=['Student_ID', 'Name', 'Email', 'Password', 'Phone', 'Registration_Date'])
        students_df = pd.concat([students_df, new_student], ignore_index=True)
        write_students(students_df)
        
        flash(f'Registration successful! Your Student ID is {student_id}. Please login.', 'success')
        return redirect(url_for('student_login'))
    
    return render_template('student_register.html')

@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        students_df = read_students()
        student = students_df[students_df['Email'] == email]
        
        if not student.empty and check_password_hash(student.iloc[0]['Password'], password):
            session['student_id'] = student.iloc[0]['Student_ID']
            session['student_name'] = student.iloc[0]['Name']
            flash('Login successful!', 'success')
            return redirect(url_for('student_home'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('student_login.html')

@app.route('/student/logout')
def student_logout():
    session.pop('student_id', None)
    session.pop('student_name', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/student')
def student_home():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    return render_template('student.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    results = None
    search_query = ''
    search_type = 'title'
    
    if request.method == 'POST':
        search_query = request.args.get('query', request.form.get('query', ''))
        search_type = request.args.get('type', request.form.get('type', 'title'))
        
        df = read_books()
        
        if search_query:
            if search_type == 'title':
                results = df[df['Title'].str.contains(search_query, case=False, na=False)]
            elif search_type == 'author':
                results = df[df['Author'].str.contains(search_query, case=False, na=False)]
            elif search_type == 'book_id':
                results = df[df['Book_ID'].str.contains(search_query, case=False, na=False)]
            
            results = results.to_dict('records')
    
    return render_template('search.html', results=results, search_query=search_query, search_type=search_type)

@app.route('/student/my_books')
def my_books():
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    student_id = session['student_id']
    issued_df = read_issued()
    
    # Get books issued to this student
    my_books = issued_df[issued_df['Student_ID'] == student_id].to_dict('records')
    
    return render_template('my_books.html', my_books=my_books)

# Librarian Routes
@app.route('/librarian/login', methods=['GET', 'POST'])
def librarian_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == LIBRARIAN_CREDS['username'] and password == LIBRARIAN_CREDS['password']:
            session['librarian'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('librarian_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('librarian_login.html')

@app.route('/librarian/logout')
def librarian_logout():
    session.pop('librarian', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/librarian/dashboard')
def librarian_dashboard():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    books_df = read_books()
    issued_df = read_issued()
    students_df = read_students()
    
    stats = {
        'total_books': len(books_df),
        'total_copies': books_df['Total_Copies'].sum(),
        'available_copies': books_df['Available_Copies'].sum(),
        'issued_books': len(issued_df[issued_df['Return_Date'] == '']),
        'total_students': len(students_df)
    }
    
    return render_template('librarian_dashboard.html', stats=stats)

@app.route('/librarian/add_book', methods=['GET', 'POST'])
def add_book():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        title = request.form.get('title')
        author = request.form.get('author')
        total_copies = int(request.form.get('total_copies'))
        
        df = read_books()
        
        # Check if book ID already exists
        if book_id in df['Book_ID'].values:
            flash('Book ID already exists!', 'error')
        else:
            new_book = pd.DataFrame([[book_id, title, author, total_copies, total_copies]], 
                                   columns=['Book_ID', 'Title', 'Author', 'Total_Copies', 'Available_Copies'])
            df = pd.concat([df, new_book], ignore_index=True)
            write_books(df)
            flash('Book added successfully!', 'success')
            return redirect(url_for('librarian_dashboard'))
    
    return render_template('add_book.html')

@app.route('/librarian/issue_book', methods=['GET', 'POST'])
def issue_book():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        student_name = request.form.get('student_name')
        student_id = request.form.get('student_id')
        
        books_df = read_books()
        
        # Check if book exists and is available
        book_row = books_df[books_df['Book_ID'] == book_id]
        
        if book_row.empty:
            flash('Book ID not found!', 'error')
        elif book_row.iloc[0]['Available_Copies'] <= 0:
            flash('No copies available!', 'error')
        else:
            # Update available copies
            books_df.loc[books_df['Book_ID'] == book_id, 'Available_Copies'] -= 1
            write_books(books_df)
            
            # Add to issued books
            issued_df = read_issued()
            issue_date = datetime.now().strftime('%Y-%m-%d')
            title = book_row.iloc[0]['Title']
            
            new_issue = pd.DataFrame([[book_id, title, student_name, student_id, issue_date, '']], 
                                    columns=['Book_ID', 'Title', 'Student_Name', 'Student_ID', 'Issue_Date', 'Return_Date'])
            issued_df = pd.concat([issued_df, new_issue], ignore_index=True)
            write_issued(issued_df)
            
            flash('Book issued successfully!', 'success')
            return redirect(url_for('librarian_dashboard'))
    
    books_df = read_books()
    available_books = books_df[books_df['Available_Copies'] > 0].to_dict('records')
    
    return render_template('issue_book.html', books=available_books)

@app.route('/librarian/return_book', methods=['GET', 'POST'])
def return_book():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        student_id = request.form.get('student_id')
        
        issued_df = read_issued()
        books_df = read_books()
        
        # Find the issued book record
        mask = (issued_df['Book_ID'] == book_id) & (issued_df['Student_ID'] == student_id) & (issued_df['Return_Date'] == '')
        
        if not issued_df[mask].empty:
            # Update return date
            return_date = datetime.now().strftime('%Y-%m-%d')
            issued_df.loc[mask, 'Return_Date'] = return_date
            write_issued(issued_df)
            
            # Update available copies
            books_df.loc[books_df['Book_ID'] == book_id, 'Available_Copies'] += 1
            write_books(books_df)
            
            flash('Book returned successfully!', 'success')
            return redirect(url_for('librarian_dashboard'))
        else:
            flash('No matching issued book found!', 'error')
    
    issued_df = read_issued()
    currently_issued = issued_df[issued_df['Return_Date'] == ''].to_dict('records')
    
    return render_template('return_book.html', issued_books=currently_issued)

@app.route('/librarian/view_issued')
def view_issued():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    issued_df = read_issued()
    all_issued = issued_df.to_dict('records')
    
    return render_template('view_issued.html', issued_books=all_issued)

@app.route('/librarian/view_students')
def view_students():
    if 'librarian' not in session:
        return redirect(url_for('librarian_login'))
    
    students_df = read_students()
    all_students = students_df.to_dict('records')
    
    return render_template('view_students.html', students=all_students)

if __name__ == '__main__':
    app.run(debug=True)
