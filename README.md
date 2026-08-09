# 📊 CSEMS - Customer Satisfaction Evaluation & Management System

A web-based **Customer Satisfaction Evaluation & Management System** designed to simplify survey creation, distribution, and analysis. Organizations can create custom surveys, collect client feedback, and analyze satisfaction metrics with ease.

## 🚀 Project Overview

The application is built with **Python**, **Flask**, and **MySQL**, following a lightweight MVC architecture. It provides separate experiences for **Administrators** and **Clients**, with each role having access to features relevant to their responsibilities.

## 👥 User Roles

### 1. Client

Clients can:

* Access survey forms via public links.
* Provide personal information (demographics, service details).
* Complete survey questionnaires with various response types.
* Submit feedback and survey responses.
* Track completion status of surveys.

### 2. Administrator

Administrators can:

* Create and manage custom survey forms.
* Add and configure survey questions (multiple question types).
* View an overview through the dashboard.
* Manage client information and responses.
* Copy or duplicate existing forms for reuse.
* Delete forms and survey data.
* View individual client responses and detailed analytics.
* Manage admin accounts and user status.
* Generate reports and satisfaction summaries.

## 📋 Key Features

| **Feature**                | **Description**                                                           |
| -------------------------- | ------------------------------------------------------------------------- |
| **Form Management**        | Create, edit, copy, and delete survey forms with full control.            |
| **Question Types**         | Support for multiple question types: short answer, paragraph, MCQ, checkbox, rating. |
| **Client Management**      | Collect and manage client demographics and service information.           |
| **Survey Distribution**    | Share survey forms with clients for feedback collection.                  |
| **Response Tracking**      | Record and track all client survey responses.                             |
| **Analytics Dashboard**    | View satisfaction metrics, response rates, and trends.                    |
| **Individual Analytics**   | Analyze responses on a per-client or per-question basis.                  |
| **Admin Dashboard**        | Overview of forms, clients, and survey metrics.                           |
| **Authentication**         | Secure login and registration with role-based access.                     |
| **Account Management**     | Manage admin profiles with status tracking (active, inactive, banned).    |
| **Data Export**            | View and analyze client responses in summary reports.                     |

## 🏗️ System Architecture

The project follows a **Model-View-Controller (MVC)** architecture optimized for Flask.

* **Controllers (Routes)** – Handle application logic and HTTP requests (defined in `app.py`).
* **Models** – Manage database operations and business data (`AdminUser`, `ClientInfo`, `SurveyQuestion`, `SurveyResponse`, `Form`).
* **Views (Templates)** – Provide the user interface in `templates/` folder.
* **Static Assets** – CSS, images, and JavaScript in `static/` folder.

## 🗄️ Database

The system uses **MySQL** to manage its core data:

* **admin_user** – Administrator accounts and profiles
* **client_info** – Client demographics and service information
* **forms** – Survey form definitions
* **survey_questions** – Questions within each form
* **survey_responses** – Client responses to survey questions

## 🔐 Demo Credentials

Use the following account to access administrator features:

| **Account**  | **Credentials** |
| ------------ | --------------- |
| **Username** | `admin`         |
| **Password** | `password`      |
| **Role**     | Administrator   |

> **Note:** These credentials are intended for local/demo use only. Change them in production.

## 🛠️ Technologies Used

* **Python 3.x**
* **Flask** (Web Framework)
* **Flask-SQLAlchemy** (ORM)
* **Flask-WTF** (Forms)
* **PyMySQL** (MySQL Driver)
* **MySQL / MariaDB** (Database)
* **HTML5**
* **CSS3**
* **JavaScript**

## 💻 How to Install & Run

### 1. Install the Requirements

Before running the project, install:

* **Python 3.8 or higher**
* **MySQL Server** (or MariaDB)
* **pip** (Python package manager, usually included with Python)

### 2. Download the Project

Clone the repository or extract the project folder:

```bash
cd path/to/CSEMS
```

### 3. Create a Virtual Environment

Create an isolated Python environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

**On Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 4. Install Python Dependencies

Install required Python packages:

```powershell
pip install -r requirements.txt
```

If `pymysql` is not included, install it separately:

```powershell
pip install pymysql
```

### 5. Configure the Database Connection

Open `app.py` and update the database configuration if needed:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ias_csm'
```

Update the following:
* **root** – Your MySQL username
* **localhost** – Your MySQL host
* **ias_csm** – Your database name
* Add your password between the colon and `@` if required: `mysql+pymysql://root:password@localhost/ias_csm`

### 6. Create the Database

Create a MySQL database for the project:

```bash
mysql -u root -p
```

Then in the MySQL prompt:

```sql
CREATE DATABASE ias_csm;
EXIT;
```

### 7. Import the Database Schema

Import the SQL schema included in the project:

```bash
mysql -u root -p ias_csm < ias_csm.sql
```

Or use the provided SQL files (`ias_csm(5).sql` or `ias_csm(6).sql`).

### 8. Start the Flask Development Server

Run the application:

```powershell
python app.py runserver
```

Or alternatively:

```powershell
python -m flask run
```

The application will be available at:

```
http://localhost:5000
```

Open this address in your web browser.

### 9. Login

Use the demo administrator account:

```
Username: admin
Password: password
```

## 📊 Survey Workflow

**Create Form → Add Questions → Assign to Clients → Clients Complete Survey → View Analytics → Export Report**

## 🎯 Project Purpose

This project demonstrates practical skills in:

* **Web Development** with Flask and Python
* **Database Design** with MySQL and SQLAlchemy ORM
* **MVC Architecture** implementation
* **CRUD Operations** (Create, Read, Update, Delete)
* **Form Management** and validation
* **User Authentication** and role-based access control
* **Survey Systems** and feedback collection
* **Analytics** and data visualization
* **RESTful API** design principles

## 📁 Project Structure

```
CSEMS/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── ias_csm(5).sql           # Database schema (version 5)
├── ias_csm(6).sql           # Database schema (version 6)
│
├── templates/               # HTML templates
│   ├── base.html           # Base template layout
│   ├── login.html          # Login page
│   ├── register.html       # Registration page
│   ├── home.html           # Admin dashboard
│   ├── questions.html      # Form and question builder
│   ├── client.html         # Client listing
│   ├── client_form.html    # Client form (survey)
│   ├── individual.html     # Individual response analytics
│   ├── summary.html        # Summary and reports
│   └── analytics.html      # Analytics dashboard
│
├── static/                 # Static assets
│   ├── css/               # Stylesheets
│   │   ├── index.css
│   │   ├── styles.css
│   │   ├── components.css
│   │   ├── font.css
│   │   └── LOGIN.CSS
│   ├── js/                # JavaScript files
│   └── images/            # Images and icons
│
└── .venv/                 # Virtual environment (created after setup)
```

## 🚨 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'pymysql'`
**Solution:** Install PyMySQL with `pip install pymysql`

### Issue: Database connection error
**Solution:** Ensure MySQL is running and credentials in `app.py` are correct.

### Issue: Virtual environment path error
**Solution:** Recreate the virtual environment:
```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate
pip install -r requirements.txt
```

## 📸 System Preview

### Login
![Login](screenshots/login.png)

## 📝 Notes

* Default database name: `ias_csm`
* Default admin credentials are for demo purposes—change them after initial setup.
* Ensure MySQL is running before starting the Flask application.
* The application uses Jinja2 templating for dynamic HTML rendering.

---

**Developed with Python, Flask, and MySQL** 🐍🔥
