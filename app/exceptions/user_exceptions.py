# the service does not decides what the user sees
# the exception  its type is the information that the service will send to the userclass
class UserException(Exception):
    """Base exception for all user-related errors."""


class EmailAlreadyExists(UserException):
    """Raised when an email is already registered."""


class UsernameAlreadyExists(UserException):
    """Raised when a username is already taken."""
class InvalidCredentials(UserException):
    """Raised when login credentials are invalid."""    