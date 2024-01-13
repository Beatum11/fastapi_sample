from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select

from data.database import get_db, AsyncSession
from data.users import User

from pydantic import BaseModel
from starlette import status

from utils.hashed_password_getter import get_hashed_password
from utils.jwt_generator import generate_jwt
from utils.jwt_checker import check_jwt

router = APIRouter()


class UserRequest(BaseModel):
    username: str
    password: str
    age: int


# GET USERS/R
@router.get('/users')
async def get_users(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        if users:
            return users
        else:
            raise HTTPException(status_code=404, detail='Cant find users, sorry!')

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Some unexpected problem: {e}')


@router.get('/users/{user_id}')
async def get_user_by_id(db: AsyncSession = Depends(get_db), user_id: int = Path(gt=0)):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if user:
            return user
        else:
            raise HTTPException(status_code=404, detail='User not found')

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Unexpected error: {e}')


# POST USER
@router.post('/users', status_code=status.HTTP_201_CREATED)
async def post_user(user_req: UserRequest, db: AsyncSession = Depends(get_db)):
    new_user = User(
        username=user_req.username,
        hashed_password=get_hashed_password(user_req.password),
        age=user_req.age
    )

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return generate_jwt(username=new_user.username,
                            user_id=new_user.id,
                            expires=timedelta(days=2))

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=404, detail=f'Unexpected error: {e}')


# PUT USER
@router.put('/users')
async def change_user_credentials(user_req: UserRequest, user_data: dict = Depends(check_jwt),
                                  db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == user_req.username))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if user.username != user_data['username']:
        raise HTTPException(status_code=403, detail='Permission denied')

    user.username = user_req.username
    user.hashed_password = get_hashed_password(user_req.password)
    user.age = user_req.age

    await db.commit()


# DELETE USER
@router.delete('/users/{user_id}')
async def delete_user(user_id: int = Path(gt=0),
                      db: AsyncSession = Depends(get_db),
                      user_data: dict = Depends(check_jwt)):

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')

    if user.username != user_data['username']:
        raise HTTPException(status_code=403, detail='Permission denied')

    await db.delete(user)
    await db.commit()
