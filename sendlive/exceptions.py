class SendLiveError(Exception):
    """Base exception for all sendlive exceptions."""


# Cloud provider related issues


class SendLiveProviderError(SendLiveError):
    """Exception raised when an error occurs related to a cloud provider such as AWS, GCP etc."""


class SendLiveProviderPermissionError(SendLiveProviderError):
    """Exception raised when a permission error is returned by a cloud provider."""
