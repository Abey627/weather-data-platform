"""
Error handling utilities for the weather application
"""
import logging
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)

def handle_api_exception(func):
    """
    Decorator to handle API exceptions uniformly
    
    Args:
        func: The view function to decorate
        
    Returns:
        function: Wrapped function with exception handling
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            logger.warning(f"Bad request: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Internal server error: {str(e)}", exc_info=True)
            return Response(
                {'error': 'An unexpected error occurred. Please try again later.'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    return wrapper
