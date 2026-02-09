# 🏗️ System Architecture - Library Management System

## Overview
The Library Management System is a Flask-based web application with dual portals for students and librarians, using Excel files for data persistence.

## Architecture Layers

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────────┐              ┌──────────────────┐    │
│  │  Student Portal  │              │ Librarian Portal │    │
│  │  - Registration  │              │  - Dashboard     │    │
│  │  - Login         │              │  - Add Books     │    │
│  │  - Search Books  │              │  - Issue Books   │    │
│  │  - My Books      │              │  - Return Books  │    │
│  └──────────────────┘              └──────────────────┘    │
│           HTML/CSS Templates with Jinja2                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                   Flask Web Framework                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Routes & Controllers                                 │  │
│  │  - @app.route('/')                                   │  │
│  │  - @app.route('/student/login')                      │  │
│  │  - @app.route('/librarian/dashboard')                │  │
│  │  - Session Management                                │  │
│  │  - Authentication & Authorization                     │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic                                       │  │
│  │  - Password Hashing (Werkzeug Security)              │  │
│  │  - Student ID Generation                             │  │
│  │  - Book Availability Calculation                     │  │
│  │  - Data Validation                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      DATA LAYER                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Data Access Functions                                │  │
│  │  - read_books() / write_books()                      │  │
│  │  - read_students() / write_students()                │  │
│  │  - read_issued() / write_issued()                    │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Pandas DataFrame Operations                         │  │
│  │  - Filtering, Searching, Updating                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PERSISTENCE LAYER                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ books.xlsx   │  │students.xlsx │  │issued_books  │     │
│  │              │  │              │  │   .xlsx      │     │
│  │ - Book_ID    │  │ - Student_ID │  │ - Book_ID    │     │
│  │ - Title      │  │ - Name       │  │ - Student_ID │     │
│  │ - Author     │  │ - Email      │  │ - Issue_Date │     │
│  │ - Copies     │  │ - Password   │  │ - Return_Date│     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│              Excel Files (openpyxl)                         │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Authentication System
- **Student Authentication**: Email/Password with hashed storage
- **Librarian Authentication**: Username/Password (configurable)
- **Session Management**: Flask sessions for maintaining login state

### 2. Student Portal Features
```
Student Registration
    ↓
Password Hashing (Werkzeug)
    ↓
Auto-generate Student ID
    ↓
Store in students.xlsx
    ↓
Login & Session Creation
    ↓
Access Portal Features:
  - Search Books
  - View My Books
  - Check Availability
```

### 3. Librarian Portal Features
```
Librarian Login
    ↓
Session Validation
    ↓
Dashboard Access:
  - View Statistics
  - Add New Books
  - Issue Books
  - Process Returns
  - View Reports
  - Manage Students
```

### 4. Data Flow - Book Issue Process
```
Librarian Selects Book & Student
    ↓
Validate Book Availability
    ↓
books.xlsx: Decrease Available_Copies
    ↓
issued_books.xlsx: Add New Record
    ↓
Update Complete
    ↓
Student Can See in "My Books"
```

### 5. Data Flow - Book Return Process
```
Librarian Enters Book_ID & Student_ID
    ↓
Find Record in issued_books.xlsx
    ↓
Update Return_Date
    ↓
books.xlsx: Increase Available_Copies
    ↓
Return Complete
    ↓
Updated in Student's History
```

## Security Features

1. **Password Hashing**
   - Uses Werkzeug's `generate_password_hash()`
   - Passwords never stored in plain text
   - Verification via `check_password_hash()`

2. **Session Management**
   - Flask secure sessions
   - Login required decorators (checks in routes)
   - Automatic session cleanup on logout

3. **Input Validation**
   - Email format validation
   - Password minimum length
   - Duplicate prevention (emails, book IDs)

## File Structure

```
app.py
├── Imports & Configuration
├── File Paths & Initialization
├── Helper Functions
│   ├── read/write operations
│   └── ID generation
├── Routes
│   ├── Home & Common
│   ├── Student Routes
│   └── Librarian Routes
└── Main Execution
```

## Data Models

### Book
- Book_ID (Primary Key, String)
- Title (String)
- Author (String)
- Total_Copies (Integer)
- Available_Copies (Integer)

### Student
- Student_ID (Primary Key, Auto-generated)
- Name (String)
- Email (Unique, String)
- Password (Hashed, String)
- Phone (String)
- Registration_Date (Date)

### Issued Book
- Book_ID (Foreign Key)
- Title (String)
- Student_Name (String)
- Student_ID (Foreign Key)
- Issue_Date (Date)
- Return_Date (Date, Nullable)

## Technology Stack

- **Backend**: Python 3.7+, Flask 3.0.0
- **Data Processing**: Pandas 2.1.4
- **Excel Operations**: openpyxl 3.1.2
- **Security**: Werkzeug 3.0.1 (password hashing)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Session Storage**: Flask server-side sessions

## Scalability Considerations

### Current Limitations
- Excel files for data storage
- Single-threaded Flask development server
- No concurrent write protection

### Recommended Upgrades for Production
1. Migrate to SQLite/PostgreSQL database
2. Implement proper ORM (SQLAlchemy)
3. Add database connection pooling
4. Deploy with production WSGI server (Gunicorn)
5. Implement proper logging
6. Add input sanitization
7. Enable HTTPS
8. Implement rate limiting
9. Add email verification
10. Create backup system

## Performance Notes

- Excel file I/O on every operation (acceptable for small-scale)
- In-memory Pandas operations (fast for typical library sizes)
- No caching implemented (can be added if needed)
- Suitable for libraries with <1000 books and <500 students

## Future Enhancement Possibilities

1. **Database Migration**: SQLite → PostgreSQL
2. **User Features**: Book reservations, renewals, fines
3. **Notifications**: Email/SMS for due dates
4. **Reports**: PDF generation, analytics
5. **API**: REST API for mobile app integration
6. **Search**: Advanced filters, full-text search
7. **Multi-library**: Support for multiple branches
8. **Barcode**: Integration with barcode scanners
