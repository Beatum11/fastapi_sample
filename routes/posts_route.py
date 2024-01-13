import json

from fastapi import HTTPException, APIRouter, Depends, Path

from data.database import AsyncSession, get_db

from starlette import status
from data.posts import Post
from data.users import User

from utils.jwt_checker import check_jwt

from pydantic import BaseModel

from users_routes import get_user_by_id
from data.redis.redis_db import get_redis
from redis import asyncio as aioredis
from data.redis.posts_schema import PostSchema


router = APIRouter()


class PostRequest(BaseModel):
    title: str
    body: str
    user_id: int


# GET POSTS FROM A USER
@router.get('/posts/{user_id}')
async def get_posts_by_user(db: AsyncSession = Depends(get_db),
                            redis: aioredis.Redis = Depends(get_redis),
                            user_id: int = Path(gt=0)):

    try:
        user = await get_user_by_id(db=db, user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail='User not found')

        if not user.posts:
            raise HTTPException(status_code=404, detail='Posts not found')

        posts = await redis.get(f'posts_{user_id}')
        if posts:
            return json.loads(posts)

        posts_schema = PostSchema(many=True)
        posts_to_dump = posts_schema.dumps(user.posts)
        await redis.set(f'posts_{user_id}', posts_to_dump, ex=3600)

        return user.posts

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {e}')


# Get Post by user_id and post_id
@router.get('/posts/{user_id}/{post_id}')
async def get_post_by_id(user_id: int = Path(gt=0),
                         post_id: int = Path(gt=0),
                         db: AsyncSession = Depends(get_db)):

    try:
        user = await get_user_by_id(user_id=user_id, db=db)
        if not user:
            raise HTTPException(status_code=404, detail='User not found!')

        for post in user.posts:
            if post.id == post_id:
                return post

        raise HTTPException(status_code=404, detail='Post not found!')

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected problem: {e}')


# CREATE A POST

@router.post('/posts/{user_id}', status_code=status.HTTP_201_CREATED)
async def create_post(post_req: PostRequest,
                      user_id: int = Path(gt=0),
                      db: AsyncSession = Depends(get_db),
                      user_data: dict = Depends(check_jwt)):

    try:
        user = await get_user_by_id(db=db, user_id=user_id)

        if user.username != user_data['username']:
            raise HTTPException(status_code=403, detail='Permission denied')

        new_post = Post(title=post_req.title, body=post_req.body, author=user)
        db.add(new_post)
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected problem: {e}')


# PUT USER'S POST

@router.put('/posts/{user_id}/{post_id}')
async def edit_post(post_req: PostRequest,
                    user_id: int = Path(gt=0),
                    post_id: int = Path(gt=0),
                    db: AsyncSession = Depends(get_db),
                    user_data: dict = Depends(check_jwt)):
    try:
        user = await get_user_by_id(db=db, user_id=user_id)

        if user.username != user_data['username']:
            raise HTTPException(status_code=403, detail='Permission denied')

        post = await get_post_by_id(user_id=user_id, post_id=post_id, db=db)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        post.title = post_req.title
        post.body = post_req.body
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected problem: {e}')


# DELETE A POST

@router.delete('/posts/{user_id}/{post_id}')
async def delete_post(user_id: int = Path(gt=0),
                      post_id: int = Path(gt=0),
                      db: AsyncSession = Depends(get_db),
                      user_data: dict = Depends(check_jwt)):
    try:
        user = await get_user_by_id(db=db, user_id=user_id)

        if user.username != user_data['username']:
            raise HTTPException(status_code=403, detail='Permission denied')

        post = await get_post_by_id(user_id=user_id, post_id=post_id, db=db)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        await db.delete(post)
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected problem: {e}')