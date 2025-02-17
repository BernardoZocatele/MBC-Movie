import jwt

SECRET_KEY = "*UgtU@66TR--pDf44e"
ALGORITHM = "HS256"

def create_jwt(user_id: int):
    payload = {"user_id": user_id}
    token = jwt.encode(payload, SECRET_KEY, algorithm = ALGORITHM)
    
    return token

