from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from starlette import status

from data.database import get_db, AsyncSession
from data.users import User
from utils.jwt_generator import generate_jwt
from services.user_authenticator import authenticate_user
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta


router = APIRouter()


@router.post('/login')
async def login_user(db: AsyncSession = Depends(get_db),
                     form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)):

    user = await authenticate_user(username=form_data.username, password=form_data.password, db=db)

    if isinstance(user, User):
        return generate_jwt(user.username, user.id, timedelta(days=2))
    else:
        raise HTTPException(status_code=401, detail='Unauthorized!!!')
