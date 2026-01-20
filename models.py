from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# 1. User Table: Stores login and profile details
class User(Base):
    __tablename__ = "Users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    account_type = Column(String(50)) # e.g., Student or Admin
    password = Column(String(255))
    
    # Relationship: One user can submit many reports
    reports = relationship("UserReport", back_populates="owner")

# 2. Admin Table: Stores administrator credentials
class Admin(Base):
    __tablename__ = "Admin"
    
    admin_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))

# 3. User Report Table: Stores faulty code submitted by users
class UserReport(Base):
    __tablename__ = "User_Report"
    
    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id")) # Linked to User table
    error_type = Column(String(100))
    language = Column(String(50))
    code_snippet = Column(Text)
    error_msg = Column(Text)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="reports")
    solution = relationship("Solution", back_populates="parent_report", uselist=False)

# 4. Solution Table: Stores the fixed code from AI or Admin
class Solution(Base):
    __tablename__ = "Solution"
    
    solution_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("User_Report.report_id")) # Linked to Report
    solution_text = Column(Text)
    step_to_fix = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Relationship back to report
    parent_report = relationship("UserReport", back_populates="solution")