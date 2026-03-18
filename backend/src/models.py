"""Database models for eSalama application"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base
import enum


class UserRole(str, enum.Enum):
    """User role enumeration"""
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"
    SYSTEM_ADMIN = "system_admin"
    GATE_SCANNER = "gate_scanner"


class DeviceType(str, enum.Enum):
    """Device type enumeration"""
    TABLET = "tablet"
    WATCH = "watch"


class AttendanceType(str, enum.Enum):
    """Attendance type enumeration"""
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


class User(Base):
    """User model for all system users"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    role = Column(SQLEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="parent", foreign_keys="Student.parent_id")
    taught_classes = relationship("Student", back_populates="teacher", foreign_keys="Student.teacher_id")


class School(Base):
    """School model"""
    __tablename__ = "schools"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    address = Column(Text)
    phone = Column(String)
    email = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    students = relationship("Student", back_populates="school")


class Student(Base):
    """Student model"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    class_name = Column(String)
    school_id = Column(Integer, ForeignKey("schools.id"))
    parent_id = Column(Integer, ForeignKey("users.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    device_id = Column(String)
    device_type = Column(SQLEnum(DeviceType))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    school = relationship("School", back_populates="students")
    parent = relationship("User", back_populates="students", foreign_keys=[parent_id])
    teacher = relationship("User", back_populates="taught_classes", foreign_keys=[teacher_id])
    attendance_records = relationship("Attendance", back_populates="student")
    location_records = relationship("LocationTracking", back_populates="student")


class Attendance(Base):
    """Attendance records"""
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(SQLEnum(AttendanceType), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    qr_code_token = Column(String)
    scanner_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")


class LocationTracking(Base):
    """GPS location tracking records"""
    __tablename__ = "location_tracking"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    accuracy = Column(Float)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("Student", back_populates="location_records")


class QRToken(Base):
    """QR code tokens"""
    __tablename__ = "qr_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    type = Column(SQLEnum(AttendanceType), nullable=False)
    is_used = Column(Boolean, default=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Notification(Base):
    """Notification records"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"))
    type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    """Audit log for tracking system actions"""
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    resource_type = Column(String)
    resource_id = Column(String)
    details = Column(Text)
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
