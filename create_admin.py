import os
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# 1. Load variables from .env
load_dotenv()

# 2. Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

# 3. Get admin info from environment variables
admin_name = os.getenv("ADMIN_NAME", "Default Admin")
admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASSWORD")

if not admin_email or not admin_password:
    print("❌ Error: Missing ADMIN_EMAIL or ADMIN_PASSWORD in .env")
    exit()

try:
    conn = sqlite3.connect(DB_PATH)
    
    # Ensure table exists
    conn.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );
    """)

    # Hash the password from .env
    password_hash = generate_password_hash(admin_password)

    # 4. Check if admin exists
    cursor = conn.execute("SELECT id FROM admins WHERE email = ?", (admin_email,))
    existing_admin = cursor.fetchone()

    if existing_admin:
        # UPDATE existing admin password/name if they already exist
        conn.execute("""
            UPDATE admins 
            SET name = ?, password_hash = ? 
            WHERE email = ?
        """, (admin_name, password_hash, admin_email))
        print(f"🔄 Admin '{admin_email}' updated with new credentials.")
    else:
        # INSERT new admin
        conn.execute("""
            INSERT INTO admins (name, email, password_hash)
            VALUES (?, ?, ?)
        """, (admin_name, admin_email, password_hash))
        print("✅ Admin account created successfully!")

    conn.commit()

except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
finally:
    if conn:
        conn.close()

print(f"   👤 Current Admin: {admin_name} ({admin_email})")
