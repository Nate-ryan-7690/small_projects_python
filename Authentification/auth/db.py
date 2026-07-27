import sqlite3
import os
from datetime import datetime, timezone, timedelta
from auth.models import User

# Path to SQLite Database file in the project root
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "auth.db")

def get_connection():
    """Open and return a new SQLite connection for one operation"""
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create the users table if it doesnt exist yet"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            reset_token TEXT,
            reset_expiry TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def create_user(username: str, email: str, password: str, role: str = "user") -> bool:
    """Create a new user in the database. Returns True if successful, False if username/email already exists"""
    created_at = datetime.now(timezone.utc).isoformat()
    conn = None
    try:    
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username, email, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password, role, created_at))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Username or email already exists
    finally:
        if conn:
            conn.close()

def get_user_by_username(username: str) -> User | None:
    """Fetch a user by username. Returns a User instance or None if not found."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        return User(**dict(row)) if row else None 
    finally:
        if conn:
            conn.close()   

def get_user_by_email(email: str) -> User | None:
    """Fetch a user by email. Returns a User instance or None if not found."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        return User(**dict(row)) if row else None 
    finally:
        if conn:
            conn.close()

def update_reset_token(user_id: int, token: str, expiry: str) -> None:
    """Update a user's reset token and expiry time."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET reset_token = ?, reset_expiry = ? WHERE user_id = ?
        """, (token, expiry, user_id))
        conn.commit()
    finally:
        if conn:
            conn.close()

def update_password(user_id: int, new_password: str) -> None:
    """Update a user's password."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users SET password = ?, reset_token = NULL, reset_expiry = NULL WHERE user_id = ?
        """, (new_password, user_id))
        conn.commit()
    finally:
        if conn:
            conn.close()