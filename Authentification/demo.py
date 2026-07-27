from auth.passwords import hash_password, verify_password
from auth.tokens import generate_token, verify_token
from auth.rbac import require_role

def main():
    password = "my_secure_password"
    hashed = hash_password(password)
    print(f"Hashed password: {hashed}")

    # Verify the password
    if verify_password(password, hashed):
        print("Password is correct!")
    else:
        print("Password is incorrect!")
"""
token = generate_token(user_id="123", username="testuser", role="admin")
print(f"Generated token: {token}")

payload = verify_token(token)
print(f"Payload: {payload}")

invalid = verify_token("invalid_token")
print(f"Invalid token payload: {invalid}")"""

@require_role("admin")
def admin_only(payload):
    return f"Welcome, {payload['username']}! You have admin access."

def user_only(payload):
    return f"Welcome, {payload['username']}! You have user access."

admin_payload = {"username": "Nate", "role": "admin"}
print(admin_only(admin_payload))
print(user_only(admin_payload))

user_payload = {"username": "Alice", "role": "user"}
print(user_only(user_payload))
try:
    print(admin_only(user_payload))
except PermissionError as e:
    print(f"Blocked: {e}")