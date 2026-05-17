# 🔐 Secure Notes Web Application

A secure web application demonstrating cybersecurity best practices and defensive implementations against common web vulnerabilities.

> **Educational Project** | Built with Flask | Protected against OWASP Top 10 vulnerabilities

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Security Controls](#security-controls)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Documentation](#documentation)
- [License](#license)

---

## 🎯 Overview

This is a comprehensive secure web application for learning and practicing secure coding principles. It includes user registration, secure authentication, and a private notes management system with built-in protections against common web attacks.

**Technology Stack:**

- Backend: Python 3.x with Flask 3.0.3
- Database: SQLite3
- Password Security: bcrypt
- Templating: Jinja2

---

## ✨ Features

### Core Functionality

- ✅ User registration with strong password policy
- ✅ Secure login with session management
- ✅ Private notes management (create, view, store)
- ✅ User logout and session termination
- ✅ Beautiful, responsive web interface

### Security Features

- ✅ **Password Hashing:** Bcrypt with automatic salt generation
- ✅ **SQL Injection Prevention:** Parameterized queries on all database operations
- ✅ **XSS Protection:** Jinja2 template autoescaping
- ✅ **Brute-Force Defense:** Account lockout (5 attempts, 2-minute lockout)
- ✅ **Input Validation:** Regex-based validation for usernames, passwords, and content
- ✅ **Session Security:** Encrypted Flask session cookies with secret key
- ✅ **User Isolation:** Foreign key constraints ensure data privacy

---

## 🛡️ Security Controls

| Security Control     | Implementation                                 | Status       |
| -------------------- | ---------------------------------------------- | ------------ |
| **Authentication**   | Username/password with bcrypt hashing          | ✅ Active    |
| **Password Policy**  | 8+ chars, uppercase, lowercase, number, symbol | ✅ Enforced  |
| **SQL Injection**    | Parameterized queries with placeholders        | ✅ Protected |
| **XSS Attacks**      | Jinja2 autoescaping on all templates           | ✅ Protected |
| **Brute-Force**      | Account lockout after 5 failed attempts        | ✅ Active    |
| **Sessions**         | Secure cookies + server-side validation        | ✅ Secured   |
| **Rate Limiting**    | 2-minute lockout after threshold               | ✅ Active    |
| **Input Validation** | Server-side validation on all inputs           | ✅ Enforced  |

---

## 📦 Requirements

- Python 3.7 or higher
- pip (Python package manager)
- ~50MB disk space
- Internet connection (for initial setup)

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**What gets installed:**

- Flask 3.0.3 - Web framework
- bcrypt 4.1.3 - Password hashing
- requests 2.32.3 - HTTP client (for testing)

### 2. Run the Application

```bash
python app.py
```

**Expected output:**

```
 * Running on http://0.0.0.0:5000
 * Debug mode: off
```

### Docker Option

Build the Docker image:

```bash
docker build -t vault-notes-app .
```

Run the container:

```bash
docker run -p 5000:5000 --env FLASK_SECRET_KEY="my-secret-key" vault-notes-app
```

Optionally, run with Docker Compose:

```bash
docker compose up --build
```

### 3. Access the Web Interface

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

You'll be redirected to the login page.

### 4. Create a Test Account

**Register Form:**

- Username: `student1` (or any 3-20 character alphanumeric username)
- Password: `StrongPass1!` (must include uppercase, lowercase, number, symbol, 8+ chars)

Click "Create Account" and you'll be redirected to login.

### 5. Login

Use the credentials you just created to log in and access the dashboard.

---

## 💻 Usage

### User Registration

1. Click "Register" on the login page
2. Enter a valid username (3-20 characters, alphanumeric + underscores)
3. Enter a strong password (8+ chars: uppercase, lowercase, number, symbol)
4. Click "Create Account"
5. You'll be redirected to login

### User Login

1. Enter your username and password
2. Click "Login"
3. On successful login, you'll see your dashboard

**Note:** After 5 failed login attempts, your account will be locked for 2 minutes.

### Managing Notes

1. On the dashboard, type your note (1-500 characters)
2. Click "Save Note"
3. Your notes appear below with creation timestamps
4. Notes are stored securely in the database

### Logout

1. Click "Logout" in the top-right corner
2. You'll be redirected to the login page
3. Your session will be terminated

---

## 🧪 Testing & Security Verification

### Automated Security Tests

After running the app (`python app.py`), open a **new terminal** and run:

```bash
python attack_tests.py
```

**What it tests:**

1. User registration functionality
2. SQL Injection vulnerability protection
3. Valid login/authentication
4. XSS (Cross-Site Scripting) prevention
5. Brute-force attack protection (6+ attempts)
6. Dictionary attack prevention

**Sample output:**

```
--- Register test user ---
Status: 200
Final URL: http://127.0.0.1:5000/register

--- SQL Injection login attempt ---
Status: 200
Final URL: http://127.0.0.1:5000/login
Contains alert tag: False

--- Brute force attempt 5: locked message present = True
```

### Manual Testing Checklist

- [ ] Register a new account
- [ ] Login with correct credentials
- [ ] Login with incorrect password (5+ times) and verify account locks
- [ ] Wait 2 minutes and verify you can login again
- [ ] Create a note with various content
- [ ] Try entering `<script>alert('test')</script>` in a note
- [ ] Verify the script appears as text, not executed
- [ ] Logout and verify you're redirected to login

---

## 📁 Project Structure

```
Cybersecurity-Implementations-Project/
├── app.py                      # Main Flask application
├── attack_tests.py             # Automated security testing suite
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
│
├── templates/                  # HTML templates
│   ├── base.html              # Master template with styling
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│   └── index.html             # Dashboard/notes page
│
├── secure_notes.db            # SQLite database (auto-created)
├── venv/                      # Python virtual environment
│
└── Documentation/

```

---

## 📚 Documentation

This project includes comprehensive documentation:

| Document                     | Purpose           | Best For                     |
| ---------------------------- | ----------------- | ---------------------------- |
| **INDEX.md**                 | Navigation guide  | Getting oriented             |
| **PROJECT_SUMMARY.txt**      | Quick reference   | Status checks, quick answers |
| **PROJECT_REPORT.md**        | Detailed analysis | Understanding architecture   |
| **ARCHITECTURE_DIAGRAMS.md** | Visual flows      | Visual learners              |
| **README.md**                | Setup & usage     | Getting started              |

**Start with INDEX.md for a guided tour of all documentation!**

---

## 🔍 Key Code Sections

### Password Hashing

```python
password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
```

### Parameterized Query (Safe)

```python
conn.execute("SELECT * FROM users WHERE username = ?", (username,))
```

### Template Autoescaping (Safe)

```jinja2
{{ note['content'] }}  {# Automatically escapes dangerous characters #}
```

### Account Lockout

```python
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 2
```

---

## ⚠️ Important Notes

1. **Development Only:** This is a development server. Do NOT use in production without proper WSGI server (Gunicorn/uWSGI) and HTTPS.

2. **Change Secret Key:** Before deployment, change the `app.secret_key` in `app.py`.

3. **Database:** The SQLite database is created automatically on first run.

4. **Testing:** Only run `attack_tests.py` on your own local application.

5. **Default Port:** The app runs on `localhost:5000`. If this port is in use, close the blocking application or change the port in `app.py`.

---

## 🐛 Troubleshooting

### "TemplateNotFound" Error

**Solution:** Make sure the `templates/` folder exists with all HTML files.

### Port Already in Use

**Solution:** Change the port in `app.py` line 198:

```python
app.run(debug=True, port=5001)  # Use port 5001 instead
```

### Database Errors

**Solution:** Delete `secure_notes.db` and run the app again to reinitialize.

### Dependencies Not Found

**Solution:** Run `pip install -r requirements.txt` again.

---

## 🎓 Learning Resources

### Understanding Security

1. **SQL Injection:** See how parameterized queries prevent injection in `app.py` lines 108-109
2. **XSS Prevention:** Study template autoescaping in the templates
3. **Password Security:** Examine bcrypt implementation in `app.py` lines 104, 139
4. **Brute-Force Protection:** Review account lockout logic in `app.py` lines 150-159
5. **Session Management:** Check Flask session handling in `app.py` lines 146-147

### OWASP Top 10 Relevance

This project demonstrates defenses against:

- A01: Broken Authentication ✅
- A02: Broken Access Control ✅
- A03: Injection ✅
- A04: Insecure Design ✅
- A07: Identification & Authentication ✅

---

## 📞 Support

### For Setup Issues

- Check Python version: `python --version`
- Verify dependencies: `pip list`
- Check if port 5000 is available: `netstat -an | find "5000"`

### For Security Questions

- Review `PROJECT_REPORT.md` for detailed security analysis
- Check `ARCHITECTURE_DIAGRAMS.md` for system flows
- See code comments in `app.py` for implementation details

---

## 📝 License

This project is for educational purposes. Use it to learn and practice secure coding principles.

---

## 🚀 Next Steps

1. **Run the application:** `python app.py`
2. **Test security:** `python attack_tests.py`
3. **Read documentation:** Start with `INDEX.md`
4. **Review code:** Study security implementations in `app.py`
5. **Experiment:** Try different payloads and verify defenses

