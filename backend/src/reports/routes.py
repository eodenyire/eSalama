"""Reports API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, date

from config.database import get_db
from src.auth.auth import get_current_user
from src.models import User, Student, Attendance, LocationTracking, Notification, UserRole

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/attendance")
async def get_attendance_report(
    school_id: Optional[int] = Query(None, description="Filter by school ID"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
    date: Optional[date] = Query(None, description="Filter by specific date"),
    start_date: Optional[date] = Query(None, description="Start of date range"),
    end_date: Optional[date] = Query(None, description="End of date range"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate attendance report with flexible filtering
    
    Permissions:
    - Admin/System Admin: Can view all attendance for their school
    - Teacher: Can view attendance for their assigned students
    - Parent: Can view attendance for their children only
    """
    # Build base query
    query = db.query(Attendance).join(Student)
    
    # Apply role-based filtering
    if current_user.role == UserRole.PARENT:
        # Parents can only see their own children
        query = query.filter(Student.parent_id == current_user.id)
    elif current_user.role == UserRole.TEACHER:
        # Teachers can see students they teach
        query = query.filter(Student.teacher_id == current_user.id)
    elif current_user.role in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        # Admins can filter by school_id if provided
        if school_id:
            query = query.filter(Student.school_id == school_id)
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Apply additional filters
    if student_id:
        query = query.filter(Student.student_id == student_id)
    
    # Date filtering
    if date:
        # Single date filter
        query = query.filter(
            db.func.date(Attendance.timestamp) == date
        )
    elif start_date and end_date:
        # Date range filter
        query = query.filter(
            Attendance.timestamp >= start_date,
            Attendance.timestamp <= end_date
        )
    elif start_date:
        query = query.filter(Attendance.timestamp >= start_date)
    elif end_date:
        query = query.filter(Attendance.timestamp <= end_date)
    
    # Order by timestamp
    query = query.order_by(Attendance.timestamp.desc())
    
    # Execute query
    attendance_records = query.all()
    
    # Format response
    report_data = []
    for record in attendance_records:
        student = db.query(Student).filter(Student.id == record.student_id).first()
        report_data.append({
            "id": record.id,
            "student_id": student.student_id if student else None,
            "student_name": student.full_name if student else None,
            "class_name": student.class_name if student else None,
            "type": record.type,
            "timestamp": record.timestamp,
            "location": {
                "lat": record.latitude,
                "lng": record.longitude
            } if record.latitude and record.longitude else None,
            "scanner_id": record.scanner_id
        })
    
    return {
        "total_records": len(report_data),
        "filters": {
            "school_id": school_id,
            "student_id": student_id,
            "date": date.isoformat() if date else None,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        },
        "data": report_data
    }


@router.get("/gps-paths")
async def get_gps_paths_report(
    student_id: str = Query(..., description="Student ID to get GPS path for"),
    date: Optional[date] = Query(None, description="Filter by specific date"),
    start_date: Optional[date] = Query(None, description="Start of date range"),
    end_date: Optional[date] = Query(None, description="End of date range"),
    limit: int = Query(1000, description="Maximum number of points to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate GPS path report for a student
    
    Permissions:
    - Admin/System Admin: Can view any student's GPS path
    - Teacher: Can view GPS paths for students they teach
    - Parent: Can view GPS paths for their children only
    """
    # Find the student
    student = db.query(Student).filter(Student.student_id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Check permissions
    if current_user.role == UserRole.PARENT:
        if student.parent_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only view your own children's GPS paths")
    elif current_user.role == UserRole.TEACHER:
        if student.teacher_id != current_user.id:
            raise HTTPException(status_code=403, detail="You can only view GPS paths for students you teach")
    elif current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Build query
    query = db.query(LocationTracking).filter(LocationTracking.student_id == student.id)
    
    # Date filtering
    if date:
        query = query.filter(db.func.date(LocationTracking.timestamp) == date)
    elif start_date and end_date:
        query = query.filter(
            LocationTracking.timestamp >= start_date,
            LocationTracking.timestamp <= end_date
        )
    elif start_date:
        query = query.filter(LocationTracking.timestamp >= start_date)
    elif end_date:
        query = query.filter(LocationTracking.timestamp <= end_date)
    
    # Order by timestamp and limit
    query = query.order_by(LocationTracking.timestamp.asc()).limit(limit)
    
    # Execute query
    locations = query.all()
    
    # Format response
    path_data = [
        {
            "timestamp": loc.timestamp,
            "lat": loc.latitude,
            "lng": loc.longitude,
            "accuracy": loc.accuracy
        }
        for loc in locations
    ]
    
    return {
        "student_id": student.student_id,
        "student_name": student.full_name,
        "total_points": len(path_data),
        "filters": {
            "date": date.isoformat() if date else None,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None
        },
        "path": path_data
    }


@router.get("/alerts")
async def get_alerts_report(
    school_id: Optional[int] = Query(None, description="Filter by school ID"),
    student_id: Optional[str] = Query(None, description="Filter by student ID"),
    date_range: Optional[str] = Query(None, description="Date range in format YYYY-MM-DD:YYYY-MM-DD"),
    type_filter: Optional[str] = Query(None, description="Filter by notification type (e.g., 'alert', 'emergency')"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Generate alerts and notifications report
    
    Permissions:
    - Admin/System Admin: Can view all alerts for their school
    - Teacher: Can view alerts for students they teach
    - Parent: Can view alerts for their children only
    """
    # Parse date range if provided
    start_date = None
    end_date = None
    if date_range:
        try:
            dates = date_range.split(":")
            if len(dates) == 2:
                start_date = datetime.fromisoformat(dates[0])
                end_date = datetime.fromisoformat(dates[1])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date range format. Use YYYY-MM-DD:YYYY-MM-DD")
    
    # Build base query - we'll use notifications as a proxy for alerts
    query = db.query(Notification).join(Student, Student.id == Notification.student_id)
    
    # Apply role-based filtering
    if current_user.role == UserRole.PARENT:
        query = query.filter(Student.parent_id == current_user.id)
    elif current_user.role == UserRole.TEACHER:
        query = query.filter(Student.teacher_id == current_user.id)
    elif current_user.role in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        if school_id:
            query = query.filter(Student.school_id == school_id)
    else:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Apply additional filters
    if student_id:
        query = query.filter(Student.student_id == student_id)
    
    if type_filter:
        query = query.filter(Notification.type.ilike(f"%{type_filter}%"))
    
    # Date filtering
    if start_date and end_date:
        query = query.filter(
            Notification.sent_at >= start_date,
            Notification.sent_at <= end_date
        )
    
    # Order by timestamp
    query = query.order_by(Notification.sent_at.desc())
    
    # Execute query
    alerts = query.all()
    
    # Format response
    alert_data = []
    for alert in alerts:
        student = db.query(Student).filter(Student.id == alert.student_id).first()
        alert_data.append({
            "id": alert.id,
            "student_id": student.student_id if student else None,
            "student_name": student.full_name if student else None,
            "type": alert.type,
            "message": alert.message,
            "sent_at": alert.sent_at,
            "is_read": alert.is_read
        })
    
    return {
        "total_alerts": len(alert_data),
        "filters": {
            "school_id": school_id,
            "student_id": student_id,
            "date_range": date_range,
            "type_filter": type_filter
        },
        "data": alert_data
    }
