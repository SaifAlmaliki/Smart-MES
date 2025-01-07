"""
Logging utilities for consistent logging across routers.
"""

from utils.logging_config import logger

def log_endpoint_access(entity_type: str, action: str, details: str = None, success: bool = True):
    """
    Log endpoint access with consistent formatting.
    
    Args:
        entity_type: Type of entity (e.g., 'Enterprise', 'Site', etc.)
        action: Action being performed (e.g., 'created', 'updated', etc.)
        details: Additional details about the action
        success: Whether the action was successful
    """
    if not details:
        details = ""
    else:
        details = f" - {details}"

    if success:
        logger.info(f"{entity_type} {action} successfully{details}")
    else:
        logger.warning(f"Failed to {action} {entity_type}{details}")

def log_entity_not_found(entity_type: str, identifier: str):
    """
    Log entity not found error with consistent formatting.
    
    Args:
        entity_type: Type of entity (e.g., 'Enterprise', 'Site', etc.)
        identifier: Identifier used to look up the entity
    """
    logger.warning(f"{entity_type} not found - {identifier}")

def log_duplicate_entity(entity_type: str, identifier: str):
    """
    Log duplicate entity error with consistent formatting.
    
    Args:
        entity_type: Type of entity (e.g., 'Enterprise', 'Site', etc.)
        identifier: Identifier that caused the duplicate
    """
    logger.warning(f"{entity_type} already exists - {identifier}")

def log_query_result(entity_type: str, count: int):
    """
    Log query results with consistent formatting.
    
    Args:
        entity_type: Type of entity (e.g., 'Enterprise', 'Site', etc.)
        count: Number of entities retrieved
    """
    logger.info(f"Retrieved {count} {entity_type}(s)")
