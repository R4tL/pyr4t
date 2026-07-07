"""Exceptions module."""

class Pyr4tError(Exception):
    """Base class for all pyr4t exceptions."""

class Pyr4tFileError(Pyr4tError):
    """Raised when a file-related error occurs in pyr4t."""

class Pyr4tRuntimeError(Pyr4tError):
    """Raised when a runtime error occurs in pyr4t."""

class Pyr4tValueError(Pyr4tError):
    """Raised when a value is invalid or unexpected."""
