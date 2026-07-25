import psycopg
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

try:
    conn = psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )

    print("✅ Connection successful!")

    cur = conn.cursor()
    cur.execute("SELECT current_database(), current_user;")

    db, user = cur.fetchone()

    print(f"📦 Database: {db}")
    print(f"👤 User: {user}")

    cur.close()
    conn.close()

    print("🔒 Connection closed.")

except Exception as e:
    print("❌ Connection failed:")
    print(e)