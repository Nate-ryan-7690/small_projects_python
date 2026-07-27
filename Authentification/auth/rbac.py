ROLE_HIERARCHY = {
    'admin': 2,
    'user': 1
}

def require_role(required_role: str):
    def decorator(func):
        def wrapper(payload: dict, *args, **kwargs):
            user_role = payload.get("role") 
            user_level = ROLE_HIERARCHY.get(user_role, 0) 
            required_level = ROLE_HIERARCHY.get(required_role, 0)  
            if user_level < required_level:
                raise PermissionError(f"Access denied: Required: {required_role}, got: {user_role}")
            return func(payload, *args, **kwargs)
        return wrapper
    return decorator
