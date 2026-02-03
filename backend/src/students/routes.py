"""Student management API routes"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from src import models, schemas
from src.auth.auth import get_current_active_user, require_role

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=schemas.StudentResponse)
async def create_student(
    student_data: schemas.StudentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "system_admin"))
):
    """Create a new student"""
    # Check if student_id already exists
    existing = db.query(models.Student).filter(
        models.Student.student_id == student_data.student_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID already exists"
        )
    
    db_student = models.Student(**student_data.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student


@router.get("/{student_id}", response_model=schemas.StudentResponse)
async def get_student(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get student by ID"""
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
            detail="Not authorized to view this student"
        )
    
    if current_user.role.value == "teacher" and student.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this student"
        )
    
    return student


@router.put("/{student_id}", response_model=schemas.StudentResponse)
async def update_student(
    student_id: str,
    student_data: schemas.StudentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "system_admin"))
):
    """Update student information"""
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Update fields
    for key, value in student_data.dict(exclude_unset=True).items():
        setattr(student, key, value)
    
    db.commit()
    db.refresh(student)
    
    return student


@router.put("/{student_id}/device", response_model=schemas.StudentResponse)
async def update_device(
    student_id: str,
    device_id: str,
    device_type: schemas.DeviceType,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "system_admin"))
):
    """Update student device information"""
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    student.device_id = device_id
    student.device_type = device_type
    
    db.commit()
    db.refresh(student)
    
    return student


@router.get("/", response_model=List[schemas.StudentResponse])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """List students (filtered by user role)"""
    query = db.query(models.Student)
    
    # Filter based on role
    if current_user.role.value == "parent":
        query = query.filter(models.Student.parent_id == current_user.id)
    elif current_user.role.value == "teacher":
        query = query.filter(models.Student.teacher_id == current_user.id)
    
    students = query.offset(skip).limit(limit).all()
    return students
