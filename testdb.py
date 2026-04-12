from sqlalchemy import create_engine

DATABASE_URL = "postgresql://ayushmanbahinipati:@localhost:5432/notes_db"

engine = create_engine(DATABASE_URL)

try:
    connection = engine.connect()
    print("✅ Connected to PostgreSQL successfully")
    connection.close()
except Exception as e:
    print("❌ Connection failed:", e)