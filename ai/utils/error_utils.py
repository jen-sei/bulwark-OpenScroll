# ai/utils/error_utils.py
import logging
import traceback
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("bulwark")

def format_error(e: Exception, context: str = None) -> Dict[str, Any]:
    """Format an exception into a standardized error object"""
    error_type = type(e).__name__
    error_message = str(e)
    
    error_obj = {
        "error_type": error_type,
        "message": error_message,
        "traceback": traceback.format_exc(),
    }
    
    if context:
        error_obj["context"] = context
    
    # Log the error
    logger.error(f"Error in {context or 'unknown context'}: {error_type} - {error_message}")
    
    return error_obj

def handle_service_error(func):
    """Decorator for handling service function errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_data = format_error(e, func.__name__)
            logger.error(f"Service error in {func.__name__}: {error_data['error_type']} - {error_data['message']}")
            
            # Return a fallback value or re-raise
            # This is where you could implement specific fallback logic
            raise
    
    return wrapper