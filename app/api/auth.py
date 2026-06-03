"""
app/api/auth.py
===============
Authentication endpoints.
 
POST /auth/token   — login with email + password, returns JWT
GET  /auth/me      — return current user's profile from JWT
POST /auth/logout  — client-side logout (blacklist handled in Redis)
POST /auth/refresh — exchange a valid token for a fresh one
 
The JWT carries: sub (employee_id), role, email, company_id, manager_id.
The role is read from the employees.department field on first login.
In production, map department → role explicitly in a roles table.
"""

from __future__ import annotations
 
from datetime import datetime, timedelta, UTC   # used for token expiration handling
from typing import Optional
 
from fastapi import APIRouter, Depends, HTTPException, status  # Used to create API routes 
from fastapi.security import OAuth2PasswordRequestForm  # This reads login from data.
from sqlalchemy import text
from jose import jwt                                   # used to create JWT tokens
import redis.asyncio as aioredis
 
from app.config import get_settings


# Load the setting from config.py, which includes secrets. 
# and router for auth endpoints.
settings = get_settings()
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Redis client for token blacklisting (logout)
'''
This client is used to store and retrieve blacklisted tokens on logout.
when an employee logs out, their JWT is added to a Redis blacklist 
with an expiration time matching the token's remaining validity.
On each authenticated request, the token is checked against this blacklist to prevent 
'''
_redis_client = None
async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    return _redis_client


# Helpers for JWT creation and verification
'''
The Employee table has different departments so we are maping to Hr, admin, Manager 
and rest of the departments are mapped to employee role.
'''
dept_to_role = {
    "HR": "hr",
    "Admin": "admin",
    "Manager": "manager",
    "finance" : "hr",
    "IT" : "employee"
}

def get_role(department: Optional[str], is_manager: bool) -> str:
    """
    Determine the users role from their department.
    Args: department, is_manager
    Returns: role (str)
    """
    dept_lower = (department or "").lower().strip()
    if dept_lower in dept_to_role:
        return dept_to_role[dept_lower]
    if is_manager:
        return "manager"    
    return "employee"


# create JWT token.
def create_access_token(
    user_id : int,
    employee_id : str,
    role : str,
    email : str,
    company_id : int,
    manager_id : Optional[int],
) -> str:
    """
    Create a JWT token with the given user information.
    Args: user_id, employee_id, role, email, company_id, manager_id
    Returns: JWT token (str)
    """
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    
    payload = {
        "sub": str(user_id),               # Users UUId(standard JWT claim)
        "employee_id": str(employee_id),        # Custom claim for employee ID
        "role": role,
        "email": email,
        "company_id": str(company_id),
        "manager_id": str(manager_id) if manager_id else None,
        "exp": int(expire.timestamp()),   # Expiration time (standard JWT claim)
        "iat": int(now.timestamp()),      # Issued at time (standard JWT claim)
    }
    
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token 


# Routes 
@ router.post("/token",
              response_model = TokenResponse,
              summary = "login with email and password, returns JWT token",
              description = ("The frontend sends email and password." 
                             "On success, returns a JWT token and user profile info."),
)

async def login(
    form : OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
): 