import os
import sqlite3
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# 1. Load variables from the .env file
load_dotenv()

# 2. Get details from environment variables
email = os.getenv("USER_EMAIL")
new_password = os.getenv("USER_PASSWORD")
db_name = os.getenv("DATABASE_NAME", "database.db")

if not email or not new_password:
    print("❌ Error: USER_EMAIL or USER_PASSWORD not found in .env file.")
else:
    try:
        # 3. Connect to your database
        conn = sqlite3.connect(db_name)

        # 4. Generate a secure hash
        pw_hash = generate_password_hash(new_password)

        # 5. Update password in the database
        cursor = conn.execute("UPDATE users SET password_hash=? WHERE email=?", (pw_hash, email))
        
        # Check if any user was actually updated
        if cursor.rowcount == 0:
            print(f"⚠️ No user found with email: {email}")
        else:
            conn.commit()
            print(f"✅ Password updated successfully for {email}!")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    finally:
        if conn:
            conn.close()
