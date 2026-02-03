"""Notification API routes"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from src import models, schemas
from src.auth.auth import get_current_active_user, require_role

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post("/")
async def send_notification(
    notification_data: schemas.NotificationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_role("admin", "system_admin", "gate_scanner"))
):
    """Send notification to user"""
    # Find student
    student = db.query(models.Student).filter(
        models.Student.student_id == notification_data.student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Determine recipients based on role
    recipients = []
    if notification_data.recipient_role.value == "parent":
        recipients.append(student.parent_id)
    elif notification_data.recipient_role.value == "teacher":
        if student.teacher_id:
            recipients.append(student.teacher_id)
    
    # Create notification records
    for recipient_id in recipients:
        db_notification = models.Notification(
            recipient_id=recipient_id,
            student_id=student.id,
            type=notification_data.type,
            message=notification_data.message
        )
        db.add(db_notification)
    
    db.commit()
    
    # TODO: Send actual push notification, SMS, or email
    
    return {"status": "success", "message": "Notifications sent"}


@router.get("/", response_model=List[schemas.NotificationResponse])
async def get_notifications(
    student_id: str = None,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get notifications for current user"""
    query = db.query(models.Notification).filter(
        models.Notification.recipient_id == current_user.id
    )
    
    if student_id:
        student = db.query(models.Student).filter(
            models.Student.student_id == student_id
        ).first()
        if student:
            query = query.filter(models.Notification.student_id == student.id)
    
    if unread_only:
        query = query.filter(models.Notification.is_read == False)
    
    notifications = query.order_by(models.Notification.sent_at.desc()).all()
    return notifications


@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Mark notification as read"""
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.recipient_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification.is_read = True
    db.commit()
    
    return {"status": "success", "message": "Notification marked as read"}
