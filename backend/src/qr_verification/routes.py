"""QR Code generation and verification API routes"""
from datetime import datetime, timedelta, timezone
import secrets
import qrcode
from io import BytesIO
import base64
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from src import models, schemas
from src.auth.auth import get_current_active_user

router = APIRouter(prefix="/qr", tags=["QR Codes"])


@router.post("/generate", response_model=schemas.QRGenerateResponse)
async def generate_qr_code(
    qr_data: schemas.QRGenerateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Generate QR code for student attendance"""
    # Find student
    student = db.query(models.Student).filter(
        models.Student.student_id == qr_data.student_id
    ).first()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Generate unique token
    token = secrets.token_urlsafe(32)
    
    # Set expiration (15 minutes from now)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    # Create QR token record
    db_token = models.QRToken(
        token=token,
        student_id=student.id,
        type=qr_data.type,
        expires_at=expires_at
    )
    
    db.add(db_token)
    db.commit()
    
    # Generate QR code image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr_content = f"{qr_data.student_id}|{qr_data.type.value}|{token}"
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    qr_code_url = f"data:image/png;base64,{img_str}"
    
    return {
        "qr_code_url": qr_code_url,
        "token": token,
        "expires_at": expires_at
    }


@router.post("/validate")
async def validate_qr_code(
    qr_data: schemas.QRValidateRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Validate QR code token"""
    # Find token
    qr_token = db.query(models.QRToken).filter(
        models.QRToken.token == qr_data.token
    ).first()
    
    if not qr_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid QR code"
        )
    
    # Check if already used
    if qr_token.is_used:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="QR code already used"
        )
    
    # Check expiration
    if qr_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="QR code has expired"
        )
    
    # Get student info
    student = db.query(models.Student).filter(
        models.Student.id == qr_token.student_id
    ).first()
    
    return {
        "status": "valid",
        "student_id": student.student_id,
        "student_name": student.full_name,
        "type": qr_token.type.value
    }
