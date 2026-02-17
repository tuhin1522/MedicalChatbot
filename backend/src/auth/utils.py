"""
Authentication Utilities
JWT token handling, password hashing, and email verification
"""

import os
import uuid
import smtplib
from datetime import datetime, timedelta
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from ..postgresql_db.models import User
from ..postgresql_db.database import get_session
from ..core import logger


# Security Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))

# Email Configuration
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "").strip("'\"")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip("'\"").replace(" ", "")  # Remove spaces from App Password
SMTP_FROM = os.getenv("SMTP_FROM", "jkkniubioattendance@gmail.com")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_password_hash(password: str) -> str:
    """
    Hash a plain password
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against hashed password
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
        
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Data to encode in token
        expires_delta: Token expiration time
        
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def decode_access_token(token: str) -> Optional[str]:
    """
    Decode JWT token and extract email
    
    Args:
        token: JWT token
        
    Returns:
        Optional[str]: Email from token or None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    """
    Get current authenticated user from JWT token
    
    Args:
        token: JWT token from request
        session: Database session
        
    Returns:
        User: Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = decode_access_token(token)
    if email is None:
        raise credentials_exception
    
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()
    
    if user is None:
        raise credentials_exception
    
    return user


def generate_verification_token() -> str:
    """
    Generate a unique verification token
    
    Returns:
        str: UUID token
    """
    return str(uuid.uuid4())


def send_verification_email(email: str, token: str) -> bool:
    """
    Send verification email to user
    
    Args:
        email: User's email address
        token: Verification token
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    verification_url = f"http://localhost:8000/auth/verify/{token}"
    
    # Check if SMTP is configured
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("SMTP not configured - printing verification link to console")
        print("="*60)
        print("📧 VERIFICATION EMAIL (SMTP NOT CONFIGURED)")
        print(f"To: {email}")
        print(f"Link: {verification_url}")
        print("="*60)
        return False
    
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔐 Verify Your Medical Chatbot Account'
        msg['From'] = SMTP_FROM
        msg['To'] = email
        
        # HTML email body
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 15px 30px; background: #667eea; 
                          color: white; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #888; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏥 Medical Chatbot</h1>
                    <p>Welcome! Please verify your email address</p>
                </div>
                <div class="content">
                    <h2>Hello!</h2>
                    <p>Thank you for registering with Medical Chatbot. To complete your registration, 
                       please verify your email address by clicking the button below:</p>
                    
                    <center>
                        <a href="{verification_url}" class="button">
                            ✅ Verify Email Address
                        </a>
                    </center>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #667eea;">{verification_url}</p>
                    
                    <p><strong>Note:</strong> This link will expire in 24 hours for security reasons.</p>
                    
                    <p>If you didn't create an account, you can safely ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2026 Medical Chatbot. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text alternative
        text = f"""
        Medical Chatbot - Email Verification
        
        Hello!
        
        Thank you for registering with Medical Chatbot. 
        Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account, you can safely ignore this email.
        
        © 2026 Medical Chatbot
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email via SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"✅ Verification email sent successfully to: {email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send verification email to {email}: {str(e)}")
        # Print to console as fallback
        print("="*60)
        print("⚠️ EMAIL SENDING FAILED - VERIFICATION LINK:")
        print(f"To: {email}")
        print(f"Link: {verification_url}")
        print(f"Error: {str(e)}")
        print("="*60)
        return False


def send_password_reset_email(email: str, token: str) -> bool:
    """
    Send password reset email to user
    
    Args:
        email: User's email address
        token: Reset token
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    reset_url = f"{FRONTEND_URL}/reset-password?token={token}"
    
    # Check if SMTP is configured
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning("SMTP not configured - printing reset link to console")
        print("="*60)
        print("📧 PASSWORD RESET EMAIL (SMTP NOT CONFIGURED)")
        print(f"To: {email}")
        print(f"Link: {reset_url}")
        print("="*60)
        return False
    
    try:
        # Create email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '🔑 Reset Your Medical Chatbot Password'
        msg['From'] = SMTP_FROM
        msg['To'] = email
        
        # HTML email body
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                          color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 15px 30px; background: #f5576c; 
                          color: white; text-decoration: none; border-radius: 5px; 
                          margin: 20px 0; font-weight: bold; }}
                .warning {{ background: #fff3cd; border-left: 4px solid #ffc107; 
                           padding: 15px; margin: 15px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #888; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏥 Medical Chatbot</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <h2>Reset Your Password</h2>
                    <p>We received a request to reset your Medical Chatbot password. 
                       Click the button below to create a new password:</p>
                    
                    <center>
                        <a href="{reset_url}" class="button">
                            🔑 Reset Password
                        </a>
                    </center>
                    
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #f5576c;">{reset_url}</p>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul>
                            <li>This link will expire in 1 hour</li>
                            <li>If you didn't request this reset, please ignore this email</li>
                            <li>Your password will remain unchanged</li>
                        </ul>
                    </div>
                </div>
                <div class="footer">
                    <p>© 2026 Medical Chatbot. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Plain text alternative
        text = f"""
        Medical Chatbot - Password Reset
        
        We received a request to reset your Medical Chatbot password.
        
        Click this link to reset your password:
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this reset, please ignore this email.
        Your password will remain unchanged.
        
        © 2026 Medical Chatbot
        """
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Send email via SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        logger.info(f"✅ Password reset email sent successfully to: {email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send password reset email to {email}: {str(e)}")
        # Print to console as fallback
        print("="*60)
        print("⚠️ EMAIL SENDING FAILED - PASSWORD RESET LINK:")
        print(f"To: {email}")
        print(f"Link: {reset_url}")
        print(f"Error: {str(e)}")
        print("="*60)
        return False
