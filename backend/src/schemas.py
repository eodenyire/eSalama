"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum


class UserRole(str, Enum):
    PARENT = "parent"
    TEACHER = "teacher"
    ADMIN = "admin"
    SYSTEM_ADMIN = "system_admin"
    GATE_SCANNER = "gate_scanner"


class DeviceType(str, Enum):
    TABLET = "tablet"
    WATCH = "watch"


class AttendanceType(str, Enum):
    ARRIVAL = "arrival"
    DEPARTURE = "departure"


# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    expires_in: int


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Student Schemas
class StudentBase(BaseModel):
    student_id: str
    full_name: str
    class_name: Optional[str] = None
    device_id: Optional[str] = None
    device_type: Optional[DeviceType] = None


class StudentCreate(StudentBase):
    school_id: int
    parent_id: int
    teacher_id: Optional[int] = None


class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    class_name: Optional[str] = None
    device_id: Optional[str] = None
    device_type: Optional[DeviceType] = None
    teacher_id: Optional[int] = None


class StudentResponse(StudentBase):
    id: int
    school_id: int
    parent_id: int
    teacher_id: Optional[int] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Location Schemas
class LocationData(BaseModel):
    lat: float
    lng: float


class LocationPost(BaseModel):
    student_id: str
    timestamp: datetime
    location: LocationData
    accuracy: Optional[float] = None


class LocationResponse(BaseModel):
    timestamp: datetime
    lat: float
    lng: float
    accuracy: Optional[float] = None
    
    class Config:
        from_attributes = True


# Attendance Schemas
class AttendanceCreate(BaseModel):
    student_id: str
    type: AttendanceType
    timestamp: datetime
    location: LocationData
    qr_code_token: str
    scanner_id: Optional[str] = None


class AttendanceResponse(BaseModel):
    id: int
    type: str
    timestamp: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Config:
        from_attributes = True


# QR Code Schemas
class QRGenerateRequest(BaseModel):
    student_id: str
    type: AttendanceType


class QRGenerateResponse(BaseModel):
    qr_code_url: str
    token: str
    expires_at: datetime


class QRValidateRequest(BaseModel):
    token: str
    scanner_id: str


# Notification Schemas
class NotificationCreate(BaseModel):
    recipient_role: UserRole
    student_id: str
    type: str
    message: str


class NotificationResponse(BaseModel):
    id: int
    type: str
    message: str
    is_read: bool
    sent_at: datetime
    
    class Config:
        from_attributes = True


# School Schemas
class SchoolCreate(BaseModel):
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class SchoolResponse(BaseModel):
    id: int
    name: str
    code: str
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
