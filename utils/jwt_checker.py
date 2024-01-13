from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from jwt_generator import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def check_jwt(token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')

        if username is None or user_id is None:
            raise HTTPException(status_code=401, detail=f"Couldn't validate credentials: {e}")

        return {'username': username, 'user_id': user_id}

    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Couldn't validate credentials: {e}")