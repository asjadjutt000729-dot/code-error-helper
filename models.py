from sqlalchemy import Column, Integer, String
from database import Base

# This class defines the structure of your SQL Server table
class ErrorLog(Base):
    __tablename__ = "error_logs" # Name of the table in SQL Server

    # Defining columns with their data types
    id = Column(Integer, primary_key=True, index=True)
    error_code = Column(String(50), nullable=False) # Ensure this name matches exactly
    description = Column(String(255), nullable=False)