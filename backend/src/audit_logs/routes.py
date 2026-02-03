"""Audit logs API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from config.database import get_db
from src.auth.auth import get_current_user
from src.models import User, AuditLog, UserRole

router = APIRouter(prefix="/audit-logs", tags=["audit-logs"])


async def create_audit_log(
    db: Session,
    user_id: int,
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[str] = None,
    ip_address: Optional[str] = None
):
    """
    Helper function to create an audit log entry
    
    This can be called from other modules to log important actions
    """
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    db.add(audit_log)
    db.commit()
    return audit_log


@router.get("")
async def get_audit_logs(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    action: Optional[str] = Query(None, description="Filter by action type"),
    resource_type: Optional[str] = Query(None, description="Filter by resource type"),
    resource_id: Optional[str] = Query(None, description="Filter by resource ID"),
    start_date: Optional[datetime] = Query(None, description="Start of date range"),
    end_date: Optional[datetime] = Query(None, description="End of date range"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Query audit logs with flexible filtering
    
    Permissions:
    - System Admin: Can view all audit logs
    - Admin: Can view audit logs for their school
    - Others: Cannot access this endpoint
    """
    # Only admins can view audit logs
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Build query
    query = db.query(AuditLog)
    
    # Apply filters
    if user_id:
        query = query.filter(AuditLog.user_id == user_id)
    
    if action:
        query = query.filter(AuditLog.action.ilike(f"%{action}%"))
    
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    
    if resource_id:
        query = query.filter(AuditLog.resource_id == resource_id)
    
    # Date filtering
    if start_date:
        query = query.filter(AuditLog.timestamp >= start_date)
    
    if end_date:
        query = query.filter(AuditLog.timestamp <= end_date)
    
    # Order by timestamp (newest first)
    query = query.order_by(AuditLog.timestamp.desc())
    
    # Apply pagination
    total_count = query.count()
    logs = query.offset(skip).limit(limit).all()
    
    # Format response
    log_data = []
    for log in logs:
        user = db.query(User).filter(User.id == log.user_id).first()
        log_data.append({
            "id": log.id,
            "user_id": log.user_id,
            "user_email": user.email if user else None,
            "user_name": user.full_name if user else None,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "details": log.details,
            "ip_address": log.ip_address,
            "timestamp": log.timestamp
        })
    
    return {
        "total_count": total_count,
        "skip": skip,
        "limit": limit,
        "logs": log_data
    }


@router.post("")
async def create_audit_log_entry(
    action: str,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    details: Optional[str] = None,
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new audit log entry
    
    Permissions:
    - Any authenticated user can create audit logs
    - Typically used by system components to log important actions
    """
    # Get IP address from request
    ip_address = None
    if request:
        ip_address = request.client.host if request.client else None
    
    # Create audit log
    audit_log = await create_audit_log(
        db=db,
        user_id=current_user.id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        details=details,
        ip_address=ip_address
    )
    
    return {
        "id": audit_log.id,
        "message": "Audit log created successfully",
        "timestamp": audit_log.timestamp
    }


@router.get("/actions")
async def get_available_actions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of distinct action types in audit logs
    
    Permissions:
    - Admin/System Admin only
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Get distinct action types
    actions = db.query(AuditLog.action).distinct().all()
    action_list = [action[0] for action in actions if action[0]]
    
    return {"actions": sorted(action_list)}


@router.get("/resource-types")
async def get_available_resource_types(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of distinct resource types in audit logs
    
    Permissions:
    - Admin/System Admin only
    """
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Get distinct resource types
    resource_types = db.query(AuditLog.resource_type).distinct().all()
    type_list = [rt[0] for rt in resource_types if rt[0]]
    
    return {"resource_types": sorted(type_list)}
