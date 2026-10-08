College Complaint Management System

A web-based College Complaint Management System built with Python, Flask, PostgreSQL, HTML, and CSS.

The system allows students to register, log in, submit complaints, and track their complaints. Administrators can log in to manage complaints and update their status.

🚀 Features
Student Features
Student registration
Student login/logout
Student dashboard
Submit complaints
View personal complaints
Track complaint status
Complaint categories
Secure session-based authentication
Admin Features
Admin login
Admin dashboard
View all complaints
View student information associated with complaints
Complaint statistics
Update complaint status
Delete/manage complaints
Admin-only protected routes
Backend Features
Flask web framework
PostgreSQL database
Environment variable configuration
Session-based authentication
Reusable authentication decorators
SQL-based data management
Foreign-key relationship between students and complaints
🛠️ Tech Stack
Technology	Purpose
Python	Backend programming
Flask	Web framework
PostgreSQL	Database
psycopg2	PostgreSQL connection
HTML5	Frontend
CSS3	Styling
Jinja2	Template rendering
python-dotenv	Environment variables
Git	Version control
GitHub	Source code hosting
📁 Project Structure
college-complaint-management-system/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   ├── student_login.html
│   ├── student_register.html
│   ├── student_dashboard.html
│   ├── submit.html
│   ├── my_complaints.html
│   ├── admin_login.html
│   └── admin_dashboard.html
│
└── static/
    └── style.css

File names may differ depending on the final project structure.

⚙️ Prerequisites

Before running the project, install the following:

Python 3.10+
PostgreSQL
Git
pip
A code editor such as VS Code

Check Python:

python --version

Check pip:

pip --version

Check Git:

git --version

Check PostgreSQL:

psql --version
📥 Installation
1. Clone the repository
git clone https://github.com/https://github.com/vinaysinghrajput2006-spec/college_complaint_system.git

Move into the project directory:

cd college-complaint-management-system
2. Create a virtual environment
Windows
python -m venv .venv

Activate it:

.venv\Scripts\activate
macOS/Linux
python3 -m venv .venv

Activate it:

source .venv/bin/activate

After activation, your terminal should show something similar to:

(.venv)
📦 Install Dependencies

Install the required Python packages:

pip install -r requirements.txt

If you haven't created requirements.txt yet, you can generate it from your development environment:

pip freeze > requirements.txt
🗄️ PostgreSQL Database Setup

Make sure PostgreSQL is installed and running.

Create a database:

CREATE DATABASE college_complaint_system;

Connect to the database:

psql -U postgres -d college_complaint_system
Database Structure

The application uses a relational database where students and complaints are connected using student_id.

Students
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    roll_number VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    department VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
Complaints
CREATE TABLE complaints (
    complaint_id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    category VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Pending',
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES students(student_id)
);

The relationship is:

students
    │
    │ student_id
    ▼
complaints

This design avoids unnecessarily duplicating student information in every complaint.

🔐 Environment Variables

The application uses a .env file for sensitive configuration such as database credentials.

Create a file named:

.env

Example:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=college_complaint_system
DB_USER=postgres
DB_PASSWORD=your_postgresql_password

SECRET_KEY=your_secret_key
Important

Never commit your .env file to GitHub.

Your .gitignore should contain:

.env
.venv/
__pycache__/
*.pyc
.vscode/
📝 .env.example

For other developers, create .env.example:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=college_complaint_system
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=your_secret_key

Developers can copy it:

copy .env.example .env

Then replace the values with their own PostgreSQL credentials.

🔑 Authentication

The application uses Flask sessions to maintain login state.

Student session

After successful student login:

session["student_id"] = student[0]

Student-only routes can be protected using:

@student_login_required
Admin session

After successful admin login:

session["admin_id"] = admin[0]

Admin-only routes can be protected using:

@admin_login_required

This prevents unauthorized users from accessing protected pages.

▶️ Running the Application

Make sure the virtual environment is activated.

Windows
.venv\Scripts\activate

Then run:

python app.py

You should see something similar to:

 * Running on http://127.0.0.1:5000

Open your browser and visit:

http://127.0.0.1:5000
🔄 Application Flow
Student Flow
Student Registration
        ↓
Student Login
        ↓
Student Dashboard
        ↓
Submit Complaint
        ↓
Complaint Stored in PostgreSQL
        ↓
My Complaints
        ↓
Track Complaint Status
Admin Flow
Admin Login
      ↓
Admin Dashboard
      ↓
View Complaints
      ↓
Review Complaint
      ↓
Update Status
      ↓
Student Sees Updated Status
📊 Complaint Status

The application can use statuses such as:

Pending
In Progress
Resolved

Example workflow:

Pending
   ↓
In Progress
   ↓
Resolved
🔗 Database Relationship

A complaint belongs to a particular student through student_id.

Example:

SELECT
    c.complaint_id,
    s.student_name,
    s.roll_number,
    s.department,
    c.category,
    c.description,
    c.status,
    c.created_at
FROM complaints c
JOIN students s
    ON c.student_id = s.student_id;

This allows the application to display student information together with complaint information without storing duplicate student data in the complaints table.

🧪 Testing

Before deploying the application, test the following:

Student

Student registration

Duplicate roll number validation

Student login

Invalid login

Student dashboard

Submit complaint

View own complaints

Student logout

Admin

Admin login

Invalid admin login

Admin dashboard

View complaints

Update complaint status

Delete complaint

Admin logout

Unauthorized access protection

Database

PostgreSQL connection

Student records

Complaint records

Foreign-key relationship

Complaint status updates

🔒 Security Notes

For production use:

Never commit .env
Never expose database passwords
Use password hashing
Validate user input
Use parameterized SQL queries
Protect admin routes
Protect student routes
Use CSRF protection
Use a strong Flask SECRET_KEY
Keep dependencies updated
Use HTTPS in production

Do not store passwords as plain text. Passwords should be stored using a secure password-hashing method such as Werkzeug's password hashing utilities.

🐛 Troubleshooting
Database connection error

Check:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=college_complaint_system
DB_USER=postgres
DB_PASSWORD=your_password

Also make sure PostgreSQL is running.

ModuleNotFoundError

For example:

ModuleNotFoundError: No module named 'flask'

Install dependencies:

pip install -r requirements.txt
PostgreSQL driver error

Make sure psycopg2 is installed:

pip install psycopg2-binary

Then verify:

python -c "import psycopg2; print(psycopg2.__version__)"
.env is not loading

Make sure:

from dotenv import load_dotenv

load_dotenv()

is called before accessing environment variables.

🌱 Future Improvements

Possible future features include:

Complaint search
Complaint filtering
Pagination
Email notifications
Complaint priority
Complaint attachments
Complaint comments
Complaint update history
Department-based complaint assignment
Admin roles
Staff accounts
Analytics and charts
REST API
Mobile-friendly UI
Deployment to a cloud platform
👨‍💻 Learning Objectives

This project demonstrates practical knowledge of:

Python
Flask
PostgreSQL
SQL
CRUD operations
Authentication
Sessions
Decorators
Jinja2 templates
HTML/CSS
Database relationships
Environment variables
Git and GitHub
Backend development
📌 Project Status

Status: In Development

This project is being developed as a BCA 5th Semester Minor Project.

📄 License

This project is intended for educational and academic purposes.

You may modify and improve it for your own learning and project requirements.

⭐ Acknowledgement

Built as a learning project to understand backend development using Python, Flask, and PostgreSQL.
