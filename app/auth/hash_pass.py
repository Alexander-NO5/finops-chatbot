import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

print(hash_password("your_password_here"))
