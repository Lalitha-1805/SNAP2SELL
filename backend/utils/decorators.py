"""
Decorators for common functionality
"""

from functools import wraps
from flask_jwt_extended import get_jwt_identity
from utils.errors import UnauthorizedError
import json


def _normalize_role(role):
    """Normalize equivalent role names between frontend and backend"""
    if not role:
        return role
    if role == 'consumer':
        return 'buyer'
    return role


def get_identity():
    """Return JWT identity as a dict when possible.

    Some versions/configurations store the identity as a JSON string in the
    token's "sub" claim. This helper parses that into a dict so existing
    code can continue to use identity.get('user_id') etc.
    """
    identity = get_jwt_identity()
    if isinstance(identity, str):
        try:
            return json.loads(identity)
        except Exception:
            return identity
    return identity


def role_required(allowed_roles):
    """Decorator to check user role"""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_identity()
            user_role = _normalize_role(identity.get('role'))
            
            # Normalize allowed roles as well for comparison
            normalized_allowed = [_normalize_role(r) for r in allowed_roles]

            if user_role not in normalized_allowed:
                raise UnauthorizedError(
                    f"Access denied. Required roles: {', '.join(allowed_roles)}"
                )
            
            return fn(*args, **kwargs)
        
        return wrapper
    return decorator


def admin_required(fn):
    """Decorator to check admin role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_identity()
        user_role = _normalize_role(identity.get('role'))
        
        if user_role != 'admin':
            raise UnauthorizedError("Admin access required")
        
        return fn(*args, **kwargs)
    
    return wrapper


def farmer_required(fn):
    """Decorator to check farmer role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_identity()
        user_role = _normalize_role(identity.get('role'))
        
        if user_role != 'farmer':
            raise UnauthorizedError("Farmer access required")
        
        return fn(*args, **kwargs)
    
    return wrapper


def buyer_required(fn):
    """Decorator to check buyer role"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        identity = get_identity()
        user_role = _normalize_role(identity.get('role'))
        
        if user_role != 'buyer':
            raise UnauthorizedError("Buyer access required")
        
        return fn(*args, **kwargs)
    
    return wrapper
