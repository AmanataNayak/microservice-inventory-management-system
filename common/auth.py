from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError

SECRET_KEY = "amanata"
ALGORITHIM = "HS256"

def get_current_user(required_role: str = None):
    async def _get_user(request: Request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
        
        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
            username = payload.get("sub")
            role = payload.get("role")
            if username is None or role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
            
            # role check
            if required_role and role != required_role:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requires role '{required_role}'")
            
            return {"username": username, "role": role}
        except JWTError:
            raise HTTPException(status_code=401, detail="Token decode error")
        
    return _get_user