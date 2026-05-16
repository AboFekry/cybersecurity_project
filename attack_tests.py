"""
Local ethical hacking test helper.
Run the Flask app first, then run: python attack_tests.py
Only test against your own local application.
"""
import requests

BASE_URL = "http://127.0.0.1:5000"


def show(name, response):
    print(f"\n--- {name} ---")
    print("Status:", response.status_code)
    print("Final URL:", response.url)
    print("Contains alert tag:", "<script>alert" in response.text.lower())
    print("Snippet:", response.text[:250].replace("\n", " "))


session = requests.Session()

# Create test user. It is okay if user already exists.
register_data = {"username": "student1", "password": "StrongPass1!"}
show("Register test user", session.post(f"{BASE_URL}/register", data=register_data, allow_redirects=True))

# SQL Injection login attempt. Expected: fail.
sqli_payload = {"username": "' OR '1'='1", "password": "anything"}
show("SQL Injection login attempt", session.post(f"{BASE_URL}/login", data=sqli_payload, allow_redirects=True))

# Correct login. Expected: success.
show("Correct login", session.post(f"{BASE_URL}/login", data=register_data, allow_redirects=True))

# XSS attempt in notes. Expected: displayed as text, not executed.
xss_payload = {"content": "<script>alert('XSS')</script>"}
show("XSS note insertion", session.post(f"{BASE_URL}/add-note", data=xss_payload, allow_redirects=True))

# Brute force simulation. Expected: account temporarily locks after repeated failures.
for i in range(1, 8):
    bad_login = {"username": "student1", "password": f"WrongPass{i}!"}
    r = session.post(f"{BASE_URL}/login", data=bad_login, allow_redirects=True)
    print(f"Brute force attempt {i}: locked message present =", "temporarily locked" in r.text.lower())

# Dictionary attack simulation. Expected: weak password guesses fail; lockout may trigger.
dictionary_words = ["password", "12345678", "student123", "qwerty", "admin123", "StrongPass1!"]
for word in dictionary_words:
    r = session.post(f"{BASE_URL}/login", data={"username": "student1", "password": word}, allow_redirects=True)
    print(f"Dictionary guess '{word}': success page reached =", "Welcome, student1" in r.text)
