"""User module with basic user management functions."""

#eshwar
class User:
    """Represents a user in the system."""

    def __init__(self, user_id: int, name: str, email: str) -> None:
        self.user_id = user_id
        self.name = name
        self.email = email
        self.is_active = True

    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False

    def get_display_name(self) -> str:
        """Return a display-friendly name with status."""
        status = "Active" if self.is_active else "Inactive"
        return f"{self.name} ({status})"

    def rename(self, new_name: str) -> None:
        """Rename the user."""
        if not new_name.strip():
            raise ValueError("Name cannot be empty")
        self.name = new_name

    def update_email(self, new_email: str) -> None:
        """Update the user's email address."""
        if "@" not in new_email:
            raise ValueError("Invalid email address")
        self.email = new_email

    def to_dict(self) -> dict:
        """Return user data as a dictionary."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "is_active": self.is_active,
        }


def validate_user_name(name: str) -> bool:
    """Check if a user name is valid (non-empty and reasonable length)."""
    return bool(name) and len(name) <= 100


def create_user(user_id: int, name: str, email: str) -> User:
    """Factory function to create a new User."""
    if not validate_user_name(name):
        raise ValueError("Invalid user name")
    return User(user_id, name, email)
