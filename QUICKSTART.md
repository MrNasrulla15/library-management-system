# 🚀 Quick Start Guide - Library Management System

## Installation

1. **Extract the ZIP file**
   ```bash
   unzip library_system.zip
   cd library_system
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 📋 Demo Accounts

### Student Account
- **Email**: john@example.com
- **Password**: student123
- **Student ID**: STU001

### Librarian Account
- **Username**: admin
- **Password**: admin123

## 🎯 First Steps

### As a Student:
1. Go to homepage → Click "Register" under Student Portal
2. Fill in your details
3. Your Student ID will be auto-generated
4. Login with email and password
5. Search for books and view your borrowing history

### As a Librarian:
1. Go to homepage → Click "Enter Librarian Portal"
2. Login with admin credentials
3. Access dashboard to:
   - Add new books
   - Issue books to students
   - Process returns
   - View issued books
   - View registered students

## 📊 Sample Data Included

The system comes pre-loaded with:
- **5 Sample Books**: Classic titles like "1984", "To Kill a Mockingbird", etc.
- **1 Demo Student**: John Doe (john@example.com)

## 🔒 Security Features

- **Password Hashing**: All student passwords are securely hashed
- **Session Management**: Secure login sessions for both students and librarians
- **Auto-generated IDs**: Unique student IDs generated automatically

## 📁 Data Storage

All data is stored in Excel files in the `data/` folder:
- `books.xlsx` - Book inventory
- `issued_books.xlsx` - Borrowing records
- `students.xlsx` - Student accounts

## 💡 Tips

- Students can search by Title, Author, or Book ID
- Librarians can see real-time availability
- The "My Books" feature shows students their complete borrowing history
- System automatically tracks issue and return dates

## ⚠️ Production Notes

Before deploying to production:
1. Change `app.secret_key` in `app.py`
2. Change librarian credentials in `LIBRARIAN_CREDS`
3. Consider migrating from Excel to a proper database (SQLite/PostgreSQL)
4. Enable HTTPS for secure password transmission

## 🆘 Troubleshooting

**Problem**: Cannot install packages
- **Solution**: Make sure you have Python 3.7+ and pip installed

**Problem**: Port 5000 already in use
- **Solution**: Change port in `app.py`: `app.run(debug=True, port=5001)`

**Problem**: Excel files not created
- **Solution**: Ensure write permissions in the project directory

## 🎉 You're Ready!

Your library management system is now ready to use. Enjoy managing your library efficiently!
