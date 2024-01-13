from fastapi import HTTPException

from sqlalchemy import select
from data.users import User
from utils.hashed_password_getter import get_crypt_context

from datetime import timedelta
from utils.jwt_generator import generate_jwt


async def authenticate_user(username: str, password: str, db):
    try:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalars().first()
        if not user:
            return False

        crypt_context = get_crypt_context()

        if not crypt_context.verify(password, user.hashed_password):
            return False

        return user

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')
    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Unexpected error: {e}')
