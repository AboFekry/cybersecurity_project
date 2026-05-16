import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import bcrypt
import re
from datetime import datetime, timedelta
from html import escape
from pathlib import Path

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key-before-deployment")
DATABASE = os.getenv("VAULT_DB", "secure_notes.db")
MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 2


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash BLOB NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            lock_until TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    conn.close()


def valid_username(username):
    return bool(re.fullmatch(r"[A-Za-z0-9_]{3,20}", username or ""))


def valid_password(password):
    # Basic strong password policy: length + upper + lower + digit + symbol
    if not password or len(password) < 8:
        return False
    return (
        re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password)
        and re.search(r"\d", password)
        and re.search(r"[^A-Za-z0-9]", password)
    )


def current_user():
    if "user_id" not in session:
        return None
    conn = get_db()
    user = conn.execute("SELECT id, username FROM users WHERE id = ?", (session["user_id"],)).fetchone()
    conn.close()
    return user


@app.before_request
def setup():
    init_db()


@app.route("/")
def index():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    conn = get_db()
    notes = conn.execute(
        "SELECT id, content, created_at FROM notes WHERE user_id = ? ORDER BY id DESC",
        (user["id"],),
    ).fetchall()
    conn.close()
    return render_template("index.html", user=user, notes=notes)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not valid_username(username):
            flash("Username must be 3-20 characters and contain only letters, numbers, or underscores.")
            return redirect(url_for("register"))

        if not valid_password(password):
            flash("Password must be at least 8 characters and include uppercase, lowercase, number, and symbol.")
            return redirect(url_for("register"))

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        conn = get_db()
        try:
            # Parameterized query prevents SQL injection.
            conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash),
            )
            conn.commit()
            flash("Account created. Please log in.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect(url_for("register"))
        finally:
            conn.close()
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        conn = get_db()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and user["lock_until"]:
            lock_until = datetime.fromisoformat(user["lock_until"])
            if datetime.utcnow() < lock_until:
                conn.close()
                flash("Account temporarily locked due to repeated failed login attempts.")
                return redirect(url_for("login"))

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            conn.execute(
                "UPDATE users SET failed_attempts = 0, lock_until = NULL WHERE id = ?",
                (user["id"],),
            )
            conn.commit()
            conn.close()
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        if user:
            failed_attempts = user["failed_attempts"] + 1
            lock_until = None
            if failed_attempts >= MAX_FAILED_ATTEMPTS:
                lock_until = (datetime.utcnow() + timedelta(minutes=LOCKOUT_MINUTES)).isoformat()
            conn.execute(
                "UPDATE users SET failed_attempts = ?, lock_until = ? WHERE id = ?",
                (failed_attempts, lock_until, user["id"]),
            )
            conn.commit()
        conn.close()
        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/add-note", methods=["POST"])
def add_note():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    content = request.form.get("content", "").strip()
    if not content or len(content) > 500:
        flash("Note must be between 1 and 500 characters.")
        return redirect(url_for("index"))

    # Store the text safely; Jinja autoescaping protects output from XSS.
    conn = get_db()
    conn.execute(
        "INSERT INTO notes (user_id, content, created_at) VALUES (?, ?, ?)",
        (user["id"], content, datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")),
    )
    conn.commit()
    conn.close()
    flash("Note added.")
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "0") == "1"
    app.run(host=host, port=port, debug=debug)
