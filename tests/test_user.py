"""Tests for the user module."""

import pytest

from app.user import User, validate_user_name, create_user


@pytest.mark.smoke
def test_user_creation() -> None:
    """Smoke test: ensure a user can be created."""
    user = User(1, "Bob", "bob@example.com")
    assert user.name == "Bob"
    assert user.email == "bob@example.com"
    assert user.is_active is True


@pytest.mark.regression
def test_user_deactivate(sample_user: User) -> None:
    """Regression test: user deactivation logic."""
    sample_user.deactivate()
    assert sample_user.is_active is False


@pytest.mark.regression
def test_user_update_email(sample_user: User) -> None:
    """Regression test: email update validation."""
    sample_user.update_email("new@example.com")
    assert sample_user.email == "new@example.com"


def test_user_update_email_invalid(sample_user: User) -> None:
    """Test that invalid email raises ValueError."""
    with pytest.raises(ValueError):
        sample_user.update_email("not-an-email")


@pytest.mark.smoke
def test_validate_user_name() -> None:
    """Smoke test: name validation."""
    assert validate_user_name("Valid Name") is True
    assert validate_user_name("") is False
    assert validate_user_name("a" * 101) is False


def test_create_user_success() -> None:
    """Test successful user creation via factory."""
    user = create_user(2, "Charlie", "charlie@example.com")
    assert user.user_id == 2


def test_create_user_invalid_name() -> None:
    """Test that invalid name raises ValueError."""
    with pytest.raises(ValueError):
        create_user(2, "", "charlie@example.com")


def test_user_to_dict(sample_user: User) -> None:
    """Test user serialization."""
    data = sample_user.to_dict()
    assert data["name"] == "Alice"
    assert "user_id" in data


@pytest.mark.smoke
def test_get_display_name_active(sample_user: User) -> None:
    """Smoke test: display name shows Active status."""
    assert sample_user.get_display_name() == "Alice (Active)"


@pytest.mark.regression
def test_get_display_name_inactive(sample_user: User) -> None:
    """Regression test: display name shows Inactive after deactivation."""
    sample_user.deactivate()
    assert sample_user.get_display_name() == "Alice (Inactive)"


@pytest.mark.smoke
def test_user_rename(sample_user: User) -> None:
    """Smoke test: renaming a user updates their name."""
    sample_user.rename("Bob")
    assert sample_user.name == "Bob"


def test_user_rename_invalid(sample_user: User) -> None:
    """Test that renaming to an empty name raises ValueError."""
    with pytest.raises(ValueError):
        sample_user.rename("   ")

