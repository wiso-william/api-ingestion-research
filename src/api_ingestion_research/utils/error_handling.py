import requests

def is_retriable_http_error(exception: Exception) -> bool:
    """Checks whether an HTTP error is considered retryable.

    Args:
        exception: Exception raised by the HTTP request.

    Returns:
        True if the exception is an HTTP error with a retryable status code,
        otherwise False.
    """
    if isinstance(exception, requests.HTTPError):
        status_code = exception.response.status_code

        return status_code in {
            429, # Rate Limit
            500, # Generic Server Error
            502, # Proxy or Gateway Error
            503, # Server is busy, down or overloaded
            504  # Proxy or Gateway is busy, down or overloaded
        }
    return False