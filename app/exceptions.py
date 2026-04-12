class DataProcessingError(Exception):
    """Base exception for the application."""


class ConfigurationError(DataProcessingError):
    """Raised when required configuration is missing or invalid."""


class ArchiveNotFoundError(DataProcessingError):
    """Raised when the archive file does not exist."""


class ExtractionError(DataProcessingError):
    """Raised when the extraction process fails."""
