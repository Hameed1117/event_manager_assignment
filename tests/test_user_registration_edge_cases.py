import pytest
from unittest.mock import patch
from pydantic import ValidationError

@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_registration_with_invalid_email(mock_send_email, db_session, email_service):
    """Test registration with invalid email formats."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Invalid email format
    with pytest.raises(ValidationError):
        user_data = {
            "email": "not-an-email",
            "password": "SecurePass123!",
            "nickname": "testuser"
        }
        from app.schemas.user_schemas import UserCreate
        user_create = UserCreate(**user_data)


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_registration_with_existing_email(mock_send_email, db_session, email_service):
    """Test registration with an email that's already registered."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Create a user first
    user_data = {
        "email": "duplicate@example.com",
        "password": "SecurePass123!",
        "nickname": "firstuser"
    }
    
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    
    # Try to create another user with the same email
    duplicate_data = {
        "email": "duplicate@example.com",  # Same email
        "password": "DifferentPass123!",
        "nickname": "seconduser"
    }
    
    duplicate_user = await UserService.create(db_session, duplicate_data, email_service)
    assert duplicate_user is None  # Should fail


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_registration_with_missing_required_fields(mock_send_email, db_session, email_service):
    """Test registration with missing required fields."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Missing email
    with pytest.raises(ValidationError):
        from app.schemas.user_schemas import UserCreate
        UserCreate(password="SecurePass123!", nickname="testuser")
    
    # Missing password
    with pytest.raises(ValidationError):
        from app.schemas.user_schemas import UserCreate
        UserCreate(email="test@example.com", nickname="testuser")


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_auto_generated_nickname(mock_send_email, db_session, email_service):
    """Test that a nickname is auto-generated if not provided."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Create user without nickname
    user_data = {
        "email": "no_nickname@example.com",
        "password": "SecurePass123!"
        # No nickname provided
    }
    
    user = await UserService.create(db_session, user_data, email_service)
    assert user is not None
    assert user.nickname is not None  # Should have auto-generated nickname
    assert len(user.nickname) > 0