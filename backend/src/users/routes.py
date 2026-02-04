"""Users management API endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from config.database import get_db
from src.auth.auth import get_current_user, get_password_hash
from src.models import User, UserRole
from src.schemas import UserResponse, UserRole as UserRoleEnum

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
async def list_users(
    role: Optional[UserRoleEnum] = Query(None, description="Filter by user role"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    search: Optional[str] = Query(None, description="Search by name or email"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    List all users with optional filtering
    
    Permissions:
    - Admin/System Admin: Can view all users in the system
    - Others: Cannot access this endpoint
    """
    # Only admins can list users
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Build query
    query = db.query(User)
    
    # Apply filters
    if role:
        query = query.filter(User.role == role)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            (User.full_name.ilike(search_filter)) | 
            (User.email.ilike(search_filter))
        )
    
    # Apply pagination
    users = query.offset(skip).limit(limit).all()
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific user by ID
    
    Permissions:
    - Admin/System Admin: Can view any user
    - Others: Can only view their own profile
    """
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="You can only view your own profile")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    full_name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information
    
    Permissions:
    - Admin/System Admin: Can update any user
    - Others: Can only update their own profile
    """
    # Check permissions
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        if current_user.id != user_id:
            raise HTTPException(status_code=403, detail="You can only update your own profile")
    
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update fields
    if full_name is not None:
        user.full_name = full_name
    if phone is not None:
        user.phone = phone
    if email is not None:
        # Check if email is already taken by another user
        existing_user = db.query(User).filter(User.email == email, User.id != user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = email
    
    db.commit()
    db.refresh(user)
    
    return user


@router.put("/{user_id}/password")
async def change_password(
    user_id: int,
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    
    Permissions:
    - Users can only change their own password
    - Admins can reset passwords for other users (current_password not required)
    """
    from src.auth.auth import verify_password
    
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check permissions
    is_admin = current_user.role in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]
    is_self = current_user.id == user_id
    
    if not (is_self or is_admin):
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Verify current password if user is changing their own password
    if is_self and not is_admin:
        if not verify_password(current_password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    # Update password
    user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


@router.delete("/{user_id}")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user account
    
    Permissions:
    - Admin/System Admin only
    
    Note: This doesn't delete the user, just sets is_active to False
    """
    # Only admins can deactivate users
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Prevent self-deactivation
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account")
    
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Deactivate
    user.is_active = False
    db.commit()
    
    return {"message": f"User {user.email} has been deactivated"}


@router.put("/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reactivate a user account
    
    Permissions:
    - Admin/System Admin only
    """
    # Only admins can activate users
    if current_user.role not in [UserRole.ADMIN, UserRole.SYSTEM_ADMIN]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    
    # Find user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Activate
    user.is_active = True
    db.commit()
    
    return {"message": f"User {user.email} has been activated"}
