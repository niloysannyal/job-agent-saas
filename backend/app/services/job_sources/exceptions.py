class JobSourceError(Exception):
    """Base exception for job source errors."""
    pass


class JobSourceConfigError(JobSourceError):
    """Raised when job source credentials or settings are missing/invalid."""
    pass


class JobSourceHTTPError(JobSourceError):
    """Raised when an external job source HTTP request fails."""
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text
