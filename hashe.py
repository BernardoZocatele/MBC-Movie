import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password_hashed, user_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), password_hashed.encode())
