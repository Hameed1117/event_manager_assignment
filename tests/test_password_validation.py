#!/usr/bin/env python3
import pytest
from app.schemas.user_schemas import UserCreate

def test_password_too_short():
    """Test that passwords shorter than 8 characters are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "Short1!",  # Only 7 characters
            "nickname": "testuser"
        }
        user_create = UserCreate(**user_data)
    
    assert "at least 8 characters" in str(excinfo.value)


def test_password_no_uppercase():
    """Test that passwords without uppercase letters are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "password123!",  # No uppercase
            "nickname": "testuser"
        }
        user_create = UserCreate(**user_data)
    
    assert "uppercase letter" in str(excinfo.value)


def test_password_no_lowercase():
    """Test that passwords without lowercase letters are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "PASSWORD123!",  # No lowercase
            "nickname": "testuser"
        }
        user_create = UserCreate(**user_data)
    
    assert "lowercase letter" in str(excinfo.value)


def test_password_no_digit():
    """Test that passwords without digits are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "Password!",  # No digit
            "nickname": "testuser"
        }
        user_create = UserCreate(**user_data)
    
    assert "digit" in str(excinfo.value)


def test_password_no_special_char():
    """Test that passwords without special characters are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "Password123",  # No special character
            "nickname": "testuser"
        }
        user_create = UserCreate(**user_data)
    
    assert "special character" in str(excinfo.value)


def test_valid_password():
    """Test that valid passwords are accepted."""
    user_data = {
        "email": "valid@example.com",
        "password": "ValidPassword123!",
        "nickname": "validuser"
    }
    user_create = UserCreate(**user_data)
    assert user_create.password == "ValidPassword123!"
