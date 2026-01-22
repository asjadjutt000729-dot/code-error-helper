from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "Users"
    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)
    email = Column(String(100))
    account_type = Column(String(50))
    password = Column(String(100))

    reports = relationship("UserReport", back_populates="owner")

class UserReport(Base):
    __tablename__ = "User_Report"
    report_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    error_type = Column(String(50))
    language = Column(String(50))
    code_snippet = Column(Text)
    error_msg = Column(Text)

    owner = relationship("User", back_populates="reports")
    # Yahan 'solution' singular rakhein taake Solution class se match kare
    solution = relationship("Solution", back_populates="parent_report", uselist=False)

class Solution(Base):
    __tablename__ = "Solution"
    # YEAHAN SPELLING THEEK KAR DI HAI: Integer
    solution_id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("User_Report.report_id"))
    solution_text = Column(Text)
    step_to_fix = Column(Text)

    parent_report = relationship("UserReport", back_populates="solution")