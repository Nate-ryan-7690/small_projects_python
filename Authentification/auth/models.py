from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    user_id: Optional[int] #None before it's saved to the Database
    username: str
    email: str
    password: str
    role: str = 'user'
    created_at: str = ''
    reset_token: Optional[str] = None
    reset_expiry: Optional[str] = None




