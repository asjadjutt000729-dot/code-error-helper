from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Connection String: Database se jurne ka rasta
SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://DESKTOP-EGH82B2/CodeErrorHelperDB?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

# 2. Database Engine banana
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

# 3. Session factory (Database se baat karne ke liye)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base class (Models banane ke liye)
Base = declarative_base()

# 5. Dependency: Database session ko open aur close karne ke liye
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()