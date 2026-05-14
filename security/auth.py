import re
import bcrypt
from datetime import datetime
from database.db import run_query
from config.settings import SETTINGS

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False

def password_strength_errors(password):
    errors = []
    if len(password) < 10:
        errors.append("Password must be at least 10 characters.")
    if not re.search(r"[A-Z]", password):
        errors.append("Add at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Add at least one lowercase letter.")
    if not re.search(r"[0-9]", password):
        errors.append("Add at least one number.")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("Add at least one symbol.")
    return errors

def ensure_default_admin():
    existing = run_query("SELECT id FROM users WHERE email=:email", {"email": SETTINGS.default_admin_email}).fetchone()
    if existing:
        return
    run_query(
        "INSERT INTO users(email,password_hash,role) VALUES(:email,:password_hash,'admin')",
        {"email": SETTINGS.default_admin_email, "password_hash": hash_password(SETTINGS.default_admin_password)}
    )

def authenticate(email, password):
    row = run_query("SELECT * FROM users WHERE email=:email", {"email": email.strip().lower()}).fetchone()
    if not row or not row.is_active:
        return None
    if verify_password(password, row.password_hash):
        run_query("UPDATE users SET last_login_at=:t WHERE id=:id", {"t": datetime.utcnow().isoformat(), "id": row.id})
        return {"id": row.id, "email": row.email, "role": row.role}
    return None

def register_user(email, password, confirm_password):
    email = email.strip().lower()
    if not EMAIL_RE.match(email):
        return False, "Enter a valid email address."
    if password != confirm_password:
        return False, "Passwords do not match."
    errors = password_strength_errors(password)
    if errors:
        return False, " ".join(errors)
    existing = run_query("SELECT id FROM users WHERE email=:email", {"email": email}).fetchone()
    if existing:
        return False, "An account with this email already exists."
    run_query(
        "INSERT INTO users(email,password_hash,role,is_active) VALUES(:email,:password_hash,'admin',1)",
        {"email": email, "password_hash": hash_password(password)}
    )
    return True, "Account created. You can now sign in."

def change_password(user_id, current_password, new_password, confirm_password):
    row = run_query("SELECT * FROM users WHERE id=:id", {"id": user_id}).fetchone()
    if not row:
        return False, "User not found."
    if not verify_password(current_password, row.password_hash):
        return False, "Current password is incorrect."
    if new_password != confirm_password:
        return False, "New passwords do not match."
    errors = password_strength_errors(new_password)
    if errors:
        return False, " ".join(errors)
    run_query(
        "UPDATE users SET password_hash=:password_hash WHERE id=:id",
        {"password_hash": hash_password(new_password), "id": user_id}
    )
    return True, "Password updated."
