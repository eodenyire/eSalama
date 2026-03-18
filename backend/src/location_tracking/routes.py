"""Location tracking API routes"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from src import models, schemas
from src.auth.auth import get_current_active_user

router = APIRouter(prefix="/location", tags=["Location"])


@router.post("/")
async def post_location(
    location_data: schemas.LocationPost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Post GPS coordinates from student device"""
    # Find student
    student = db.query(models.Student).filter(
        models.Student.student_id == location_data.student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Create location record
    db_location = models.LocationTracking(
        student_id=student.id,
        latitude=location_data.location.lat,
        longitude=location_data.location.lng,
        accuracy=location_data.accuracy,
        timestamp=location_data.timestamp
    )
    
    db.add(db_location)
    db.commit()
    
    return {"status": "success", "message": "Location recorded"}


@router.get("/{student_id}/last", response_model=schemas.LocationResponse)
async def get_last_location(
    student_id: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get last known location of student"""
    # Find student
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
            detail="Not authorized to view this student's location"
        )
    
    # Get last location
    last_location = db.query(models.LocationTracking).filter(
        models.LocationTracking.student_id == student.id
    ).order_by(models.LocationTracking.timestamp.desc()).first()
    
    if not last_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No location data available"
        )
    
    return {
        "timestamp": last_location.timestamp,
        "lat": last_location.latitude,
        "lng": last_location.longitude,
        "accuracy": last_location.accuracy
    }


@router.get("/{student_id}/history", response_model=List[schemas.LocationResponse])
async def get_location_history(
    student_id: str,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get location history for a student"""
    # Find student
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
            detail="Not authorized to view this student's location"
        )
    
    # Get location history
    locations = db.query(models.LocationTracking).filter(
        models.LocationTracking.student_id == student.id
    ).order_by(models.LocationTracking.timestamp.desc()).limit(limit).all()
    
    return [
        {
            "timestamp": loc.timestamp,
            "lat": loc.latitude,
            "lng": loc.longitude,
            "accuracy": loc.accuracy
        }
        for loc in locations
    ]
