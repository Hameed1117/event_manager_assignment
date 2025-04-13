import pytest
from app.schemas.user_schemas import UserCreate
from unittest.mock import patch, MagicMock

def test_nickname_with_invalid_characters():
    """Test that nicknames with invalid characters are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "nickname": "test@user"  # Contains @ which is not allowed
        }
        user_create = UserCreate(**user_data)
    
    # Check that we get a validation error for the pattern
    assert "String should match pattern" in str(excinfo.value)


def test_nickname_too_short():
    """Test that nicknames that are too short are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "nickname": "ab"  # Only 2 characters
        }
        user_create = UserCreate(**user_data)
    
    assert "at least 3 characters" in str(excinfo.value)


def test_nickname_too_long():
    """Test that nicknames that are too long are rejected."""
    with pytest.raises(ValueError) as excinfo:
        user_data = {
            "email": "test@example.com",
            "password": "SecurePass123!",
            "nickname": "a" * 51  # 51 characters
        }
        user_create = UserCreate(**user_data)
    
    # Check that we get a validation error for string length
    assert "String should have at most 50 characters" in str(excinfo.value)


# For the tests involving database operations, we'll use mocking to avoid SMTP issues
@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_duplicate_nickname(mock_send_email, db_session, email_service):
    """Test that duplicate nicknames are rejected."""
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Create a user first
    user_data_1 = {
        "email": "test1@example.com",
        "password": "SecurePass123!",
        "nickname": "testuser"
    }
    
    from app.services.user_service import UserService
    await UserService.create(db_session, user_data_1, email_service)
    
    # Try to create another user with the same nickname
    user_data_2 = {
        "email": "test2@example.com",
        "password": "SecurePass123!",
        "nickname": "testuser"  # Same nickname
    }
    
    result = await UserService.create(db_session, user_data_2, email_service)
    assert result is None  # The create method should return None for duplicate nicknames


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_valid_nickname(mock_send_email, db_session, email_service):
    """Test that valid nicknames are accepted."""
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    user_data = {
        "email": "valid@example.com",
        "password": "SecurePass123!",
        "nickname": "valid_user123"
    }
    
    from app.services.user_service import UserService
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.nickname == "valid_user123"