"""
User Authentication Routes
Endpoints for user registration, login, verification, and password reset
"""

from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse, JSONResponse
from sqlmodel import Session, select

from ...core import logger
from ...postgresql_db.models import User, UserCreate, UserSchema, Token, ForgotPasswordRequest, ResetPasswordRequest
from ...postgresql_db.database import get_session
from ...auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
    generate_verification_token,
    send_verification_email,
    send_password_reset_email,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    FRONTEND_URL
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    
    Args:
        user_in: User registration data
        session: Database session
        
    Returns:
        UserSchema: Created user data
        
    Raises:
        HTTPException: If email already registered
    """
    logger.info(f"Registration attempt for email: {user_in.email}")
    
    # Check if user already exists
    statement = select(User).where(User.email == user_in.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        logger.warning(f"Registration failed: Email already registered - {user_in.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash password and create verification token
    hashed_password = get_password_hash(user_in.password)
    verification_token = generate_verification_token()
    
    # Create new user
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        password_hash=hashed_password,
        verification_token=verification_token,
        is_verified=False
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Send verification email (returns success status)
    email_sent = send_verification_email(new_user.email, verification_token)
    
    if email_sent:
        logger.info(f"User registered successfully with email sent: {new_user.email}")
    else:
        logger.warning(f"User registered but email failed - manual verification needed: {new_user.email}")
        logger.info(f"Verification link: http://localhost:8000/auth/verify/{verification_token}")
    
    return new_user


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """
    Login user and return JWT token
    
    Args:
        form_data: OAuth2 form with username (email) and password
        session: Database session
        
    Returns:
        Token: JWT access token
        
    Raises:
        HTTPException: If credentials are invalid or email not verified
    """
    logger.info(f"Login attempt for email: {form_data.username}")
    
    # Find user by email
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(f"Login failed: Invalid credentials - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
    
    # Check if email is verified
    if not user.is_verified:
        logger.warning(f"Login failed: Email not verified - {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified. Please check your inbox for verification link."
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in successfully: {user.email}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/verify/{token}")
async def verify_email(token: str, request: Request, session: Session = Depends(get_session)):
    """
    Verify user email with token - redirects browsers, returns JSON for API calls
    
    Args:
        token: Verification token from email
        request: FastAPI request to check Accept header
        session: Database session
        
    Returns:
        RedirectResponse for browsers or JSONResponse for API calls
    """
    logger.info(f"Email verification attempt with token: {token[:10]}...")
    
    # Check if request is from browser or API (fetch)
    accept_header = request.headers.get('accept', '')
    is_browser = 'text/html' in accept_header
    
    # Find user by verification token
    statement = select(User).where(User.verification_token == token)
    user = session.exec(statement).first()
    
    if not user:
        logger.warning(f"Email verification failed: Invalid token")
        if is_browser:
            return RedirectResponse(
                url=f"{FRONTEND_URL}/verify-email?token={token}&status=error&message=Invalid+verification+token",
                status_code=303
            )
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": "Invalid verification token"}
        )
    
    # Check if already verified
    if user.is_verified:
        logger.info(f"Email already verified: {user.email}")
        if is_browser:
            return RedirectResponse(
                url=f"{FRONTEND_URL}/verify-email?token={token}&status=success&message=Email+already+verified",
                status_code=303
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": "Email already verified. You can now login."}
        )
    
    # Mark as verified
    user.is_verified = True
    session.add(user)
    session.commit()
    
    logger.info(f"Email verified successfully: {user.email}")
    if is_browser:
        return RedirectResponse(
            url=f"{FRONTEND_URL}/verify-email?token={token}&status=success&message=Email+verified+successfully",
            status_code=303
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "success", "message": "Email verified successfully. You can now login."}
    )


@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    session: Session = Depends(get_session)
):
    """
    Request password reset link
    
    Args:
        request: Email for password reset
        session: Database session
        
    Returns:
        dict: Success message
        
    Note:
        Always returns success to prevent email enumeration
    """
    logger.info(f"Password reset requested for: {request.email}")
    
    # Find user by email
    statement = select(User).where(User.email == request.email)
    user = session.exec(statement).first()
    
    # Always return success even if user not found (prevent enumeration)
    if user:
        # Generate reset token
        reset_token = generate_verification_token()
        user.verification_token = reset_token
        session.add(user)
        session.commit()
        
        # Send reset email
        send_password_reset_email(user.email, reset_token)
        logger.info(f"Password reset email sent to: {user.email}")
    else:
        logger.info(f"Password reset requested for non-existent email: {request.email}")
    
    return {
        "message": "If an account exists with that email, a password reset link has been sent."
    }


@router.post("/reset-password")
async def reset_password(
    request: ResetPasswordRequest,
    session: Session = Depends(get_session)
):
    """
    Reset password with token
    
    Args:
        request: Reset token and new password
        session: Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If token is invalid
    """
    logger.info(f"Password reset attempt with token: {request.token[:10]}...")
    
    # Find user by reset token
    statement = select(User).where(User.verification_token == request.token)
    user = session.exec(statement).first()
    
    if not user:
        logger.warning("Password reset failed: Invalid token")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Update password
    hashed_password = get_password_hash(request.new_password)
    user.password_hash = hashed_password
    user.verification_token = None  # Clear token
    session.add(user)
    session.commit()
    
    logger.info(f"Password reset successfully: {user.email}")
    return {"message": "Password reset successfully. You can now login with your new password."}


@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user
    
    Args:
        current_user: Current authenticated user from token
        
    Returns:
        UserSchema: Current user data
    """
    logger.info(f"User profile accessed: {current_user.email}")
    return current_user


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    """
    Logout current user
    
    Note: Since we're using JWT tokens, actual logout is handled client-side.
    This endpoint is mainly for logging purposes and future enhancements
    (like token blacklisting if needed).
    
    Args:
        current_user: Current authenticated user from token
        
    Returns:
        dict: Success message
    """
    logger.info(f"User logged out: {current_user.email}")
    return {"message": "Logged out successfully"}
