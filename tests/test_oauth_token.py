import pytest
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