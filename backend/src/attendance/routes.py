"""Attendance management API routes"""
from typing import List, Optional
from datetime import date, datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from config.database import get_db
from src import models, schemas
from src.auth.auth import get_current_active_user

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=schemas.AttendanceResponse)
async def record_attendance(
    attendance_data: schemas.AttendanceCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Record student arrival or departure"""
    # Find student
    student = db.query(models.Student).filter(
        models.Student.student_id == attendance_data.student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Verify QR token
    qr_token = db.query(models.QRToken).filter(
        models.QRToken.token == attendance_data.qr_code_token,
        models.QRToken.is_used.is_(False)
    ).first()
    
    if not qr_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired QR code"
        )
    
    if qr_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="QR code has expired"
        )
    
    # Mark token as used
    qr_token.is_used = True
    
    # Create attendance record
    db_attendance = models.Attendance(
        student_id=student.id,
        type=attendance_data.type,
        timestamp=attendance_data.timestamp,
        latitude=attendance_data.location.lat,
        longitude=attendance_data.location.lng,
        qr_code_token=attendance_data.qr_code_token,
        scanner_id=attendance_data.scanner_id
    )
    
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    
    # TODO: Send notification to parent and teacher
    
    return db_attendance


@router.get("/", response_model=List[schemas.AttendanceResponse])
async def get_attendance(
    student_id: Optional[str] = Query(None),
    date: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get attendance records"""
    query = db.query(models.Attendance)
    
    if student_id:
        student = db.query(models.Student).filter(
            models.Student.student_id == student_id
        ).first()
        
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found"
            )
        
        # Check permissions
        if current_user.role.value == "parent" and student.parent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this student's attendance"
            )
        
        query = query.filter(models.Attendance.student_id == student.id)
    
    if date:
        # Filter by date
        start_of_day = datetime.combine(date, datetime.min.time())
        end_of_day = datetime.combine(date, datetime.max.time())
        query = query.filter(
            models.Attendance.timestamp >= start_of_day,
            models.Attendance.timestamp <= end_of_day
        )
    
    attendance_records = query.order_by(models.Attendance.timestamp.desc()).all()
    return attendance_records
