# tests/test_oauth_token.py
import pytest
from unittest.mock import patch
import jwt
from datetime import datetime, timedelta
from app.utils.security import create_access_token, verify_token

def test_create_access_token():
    """Test creating an access token."""
    # Create token
    token = create_access_token("test_user")
    
    # Verify it's a string
    assert isinstance(token, str)
    
    # Decode and verify subject
    decoded = jwt.decode(token, options={"verify_signature": False})
    assert decoded["sub"] == "test_user"
    
    # Verify expiration is set
    assert "exp" in decoded


def test_token_expiration():
    """Test token expiration time is set correctly."""
    # Generate a token with a custom expiration time (10 minutes)
    token = create_access_token("test_subject", expires_delta=timedelta(minutes=10))
    
    # Decode the token without verification to check the expiration
    decoded = jwt.decode(token, options={"verify_signature": False})
    
    # Check expiration is set correctly (within a small margin to account for processing time)
    exp_time = datetime.fromtimestamp(decoded["exp"])
    expected_time = datetime.utcnow() + timedelta(minutes=10)
    
    # Allow for a 10-second margin of error in the token expiration time
    assert abs((exp_time - expected_time).total_seconds()) < 10


def test_verify_token():
    """Test token verification."""
    # Create token
    token = create_access_token("test_user")
    
    # Verify token is valid
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded["sub"] == "test_user"


def test_invalid_token_format():
    """Test handling of tokens with invalid format."""
    invalid_token = "not.a.valid.token"
    
    # Verify the token is rejected
    decoded = verify_token(invalid_token)
    assert decoded is None


def test_expired_token():
    """Test handling of expired tokens."""
    # Generate a token that is already expired
    token = create_access_token("test_subject", expires_delta=timedelta(seconds=-10))
    
    # Verify the token is rejected
    decoded = verify_token(token)
    assert decoded is None


def test_malformed_token():
    """Test handling of malformed tokens."""
    # Construct a malformed token
    malformed_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIifQ"  # Missing signature part
    
    # Verify the token is rejected
    decoded = verify_token(malformed_token)
    assert decoded is Noneimport pytest
from datetime import timedelta
import time
import jwt

# Direct import testing approach - avoids dependency issues
def test_token_functionality():
    """Test basic JWT token functionality."""
    # Import locally to avoid dependency issues
    from app.utils.security import create_access_token
    
    # Create token
    user_id = "test123"
    token = create_access_token(user_id)
    assert isinstance(token, str)
    
    # Decode token manually
    secret_key = "your-secret-key-for-development-only"  # Must match what's in security.py
    decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
    assert decoded["sub"] == user_id
    
    # Verify expiration works
    assert "exp" in decoded