import pytest
from unittest.mock import patch
from app.schemas.user_schemas import UserUpdate

@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_update_bio_only(mock_send_email, db_session, email_service, user):
    """Test updating only the bio field."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Update only the bio
    update_data = {
        "bio": "This is my new bio"
    }
    
    updated_user = await UserService.update(db_session, user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.bio == "This is my new bio"
    # Other fields should remain unchanged
    assert updated_user.nickname == user.nickname
    assert updated_user.profile_picture_url == user.profile_picture_url


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_update_profile_picture_only(mock_send_email, db_session, email_service, user):
    """Test updating only the profile picture URL."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Update only the profile picture URL
    update_data = {
        "profile_picture_url": "https://example.com/new-pic.jpg"
    }
    
    updated_user = await UserService.update(db_session, user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.profile_picture_url == "https://example.com/new-pic.jpg"
    # Other fields should remain unchanged
    assert updated_user.nickname == user.nickname
    assert updated_user.bio == user.bio


@pytest.mark.asyncio
@patch('app.services.email_service.EmailService.send_verification_email')
async def test_update_multiple_fields(mock_send_email, db_session, email_service, user):
    """Test updating both bio and profile picture URL simultaneously."""
    from app.services.user_service import UserService
    
    # Make the email sending a no-op
    mock_send_email.return_value = None
    
    # Update both fields
    update_data = {
        "bio": "Updated bio text",
        "profile_picture_url": "https://example.com/updated-pic.jpg"
    }
    
    updated_user = await UserService.update(db_session, user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.bio == "Updated bio text"
    assert updated_user.profile_picture_url == "https://example.com/updated-pic.jpg"
    # Nickname should remain unchanged
    assert updated_user.nickname == user.nickname


def test_bio_too_long():
    """Test that bios that are too long are rejected."""
    # Create a bio that is too long (e.g., over 500 characters)
    long_bio = "a" * 501
    
    with pytest.raises(ValueError) as excinfo:
        update_data = UserUpdate(bio=long_bio)
    
    assert "String should have at most 500 characters" in str(excinfo.value)


def test_invalid_profile_picture_url():
    """Test that invalid profile picture URLs are rejected."""
    # Invalid URL
    with pytest.raises(ValueError) as excinfo:
        update_data = UserUpdate(profile_picture_url="not-a-valid-url")
    
    assert "Invalid URL format" in str(excinfo.value) or "URL" in str(excinfo.value)