# 📚 Library Management System

A comprehensive web-based Library Management System built with Python Flask, featuring separate portals for students and librarians.

## ✨ Features

### 👩‍🎓 Student Portal
- **Secure Registration & Login**: Create account with email and password
- **Password Hashing**: Secure password storage using Werkzeug
- **Search Books**: Search by Title, Author, or Book ID
- **View Availability**: Real-time availability status
- **My Books**: Track personally borrowed books and history
- **User Dashboard**: Personalized portal with student information

### 👨‍🏫 Librarian Portal
- **Secure Login**: Username and password authentication
- **Add Books**: Add new books to the library collection
- **Issue Books**: Issue books to students with tracking
- **Return Books**: Process book returns and update inventory
- **View Reports**: Complete history of all issued books
- **Dashboard**: Overview of library statistics
- **Student Management**: View all registered students

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML5, CSS3
- **Data Storage**: Excel (using openpyxl and pandas)
- **Styling**: Custom CSS with responsive design

## 📦 Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory**
   ```bash
   cd library_system
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and go to: `http://127.0.0.1:5000`

## 🔐 Default Credentials

**Librarian Login:**
- Username: `admin`
- Password: `admin123`

**Demo Student Account:**
- Email: `john@example.com`
- Password: `student123`
- Student ID: `STU001`

> ⚠️ **Important**: Change these credentials in production by modifying the `LIBRARIAN_CREDS` dictionary in `app.py`

## 📁 Project Structure

```
library_system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── data/                       # Data storage directory
│   ├── books.xlsx             # Books database
│   ├── issued_books.xlsx      # Issued books records
│   └── students.xlsx          # Student accounts
├── static/
│   └── css/
│       └── style.css          # Styling
└── templates/                  # HTML templates
    ├── base.html              # Base template
    ├── home.html              # Home page
    ├── student_register.html  # Student registration
    ├── student_login.html     # Student login
    ├── student.html           # Student portal
    ├── search.html            # Search results
    ├── my_books.html          # Student's borrowed books
    ├── librarian_login.html   # Librarian login
    ├── librarian_dashboard.html
    ├── add_book.html
    ├── issue_book.html
    ├── return_book.html
    └── view_issued.html
```

## 📊 Data Files

The system automatically creates three Excel files in the `data/` directory:

### books.xlsx
Stores all book information:
- Book_ID
- Title
- Author
- Total_Copies
- Available_Copies

### issued_books.xlsx
Tracks all book issues:
- Book_ID
- Title
- Student_Name
- Student_ID
- Issue_Date
- Return_Date

### students.xlsx
Stores student accounts:
- Student_ID (auto-generated)
- Name
- Email
- Password (hashed)
- Phone
- Registration_Date

## 🚀 Usage Guide

### For Students

**First Time Users:**
1. Click on **Student Portal** → **Register**
2. Fill in your details (name, email, password, phone)
3. Your Student ID will be auto-generated
4. Login with your email and password

**Returning Users:**
1. Click on **Student Portal** → **Login**
2. Enter your email and password
3. Access your personalized dashboard

**Features:**
- **Search Books**: Find books by title, author, or ID
- **My Books**: View your borrowing history and currently borrowed books
- **View Availability**: Check real-time book availability

### For Librarians

1. Click on **Librarian Portal** from the home page
2. Login with credentials
3. Access the dashboard with these options:

   **Add New Book**
   - Enter Book ID, Title, Author, and number of copies
   - Submit to add to collection

   **Issue Book**
   - Select book from dropdown
   - Enter student name and ID
   - Submit to issue

   **Return Book**
   - Enter Book ID and Student ID
   - Submit to process return

   **View Issued Books**
   - See complete history
   - Filter by status (Issued/Returned)

## 🎨 Features Highlights

- **Secure Authentication**: Password hashing with Werkzeug security
- **Student Accounts**: Self-registration with auto-generated Student IDs
- **Personalized Experience**: Students can track their own borrowed books
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Immediate reflection of changes
- **Data Validation**: Prevents duplicate Book IDs and emails
- **User Feedback**: Success/error messages for all actions
- **Clean UI**: Modern gradient design with smooth animations
- **Sample Data**: Pre-loaded with sample books and a demo student account

## 🔧 Customization

### Change Login Credentials
Edit in `app.py`:
```python
LIBRARIAN_CREDS = {'username': 'your_username', 'password': 'your_password'}
```

### Change Secret Key
Edit in `app.py`:
```python
app.secret_key = 'your_secure_secret_key'
```

### Add More Sample Books
Modify the `sample_books` list in the `init_files()` function in `app.py`

## 🐛 Troubleshooting

**Issue**: Excel files not being created
- **Solution**: Ensure write permissions in the project directory

**Issue**: Module not found errors
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Port already in use
- **Solution**: Change the port in `app.py`: `app.run(debug=True, port=5001)`

## 📝 Future Enhancements

Potential features for future versions:
- [ ] Multiple librarian accounts
- [ ] Fine calculation for overdue books
- [ ] Student login system
- [ ] Book reservation system
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Export reports to PDF
- [ ] Database migration (SQLite/PostgreSQL)

## 📄 License

This project is open-source and available for educational purposes.

## 👨‍💻 Developer Notes

- The system uses Flask sessions for authentication
- Excel files are created automatically on first run
- All date operations use datetime module
- Pandas is used for efficient data manipulation

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

---

**Made with ❤️ for library management**
