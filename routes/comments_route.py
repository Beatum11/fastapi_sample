from fastapi import HTTPException, APIRouter, Depends, Path

from data.database import AsyncSession, get_db

from starlette import status
from data.posts import Post
from data.users import User

from utils.jwt_checker import check_jwt

from pydantic import BaseModel, Field

from users_routes import get_user_by_id
from sqlalchemy import select
from users_routes import get_user_by_id
from posts_route import get_post_by_id
from data.comments import Comment


router = APIRouter()


class CommentRequest(BaseModel):
    body: str = Field(min_length=5)
    author_id: int = Field(min_length=1)


# GET COMMENTS BY POST

@router.get('/{post_id}/comments')
async def get_comments_by_post(post_id: int = Path(gt=0), db: AsyncSession = Depends(get_db)):
    try:
        post_res = await db.execute(select(Post).where(Post.id == post_id))
        post = post_res.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        return post.comments

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {e}')


# POST A COMMENT

@router.post('/{user_id}/{post_id}/comments', status_code=status.HTTP_201_CREATED)
async def create_comment(comment_req: CommentRequest, user_id: int = Path(gt=0),
                         post_id: int = Path(gt=0),
                         user_data: dict = Depends(check_jwt),
                         db: AsyncSession = Depends(get_db)):
    try:
        # I have to find a user that made this comment
        user_that_made_comm = await get_user_by_id(db=db, user_id=comment_req.author_id)
        if not user_that_made_comm:
            raise HTTPException(status_code=404, detail='User not found')

        if user_that_made_comm.username != user_data['username']:
            raise HTTPException(status_code=403, detail='Permission denied')

        post = await get_post_by_id(db=db, post_id=post_id, user_id=user_id)
        if not post:
            raise HTTPException(status_code=404, detail='Post not found')

        comment = Comment(body=comment_req.body, author_id=comment_req.author_id,
                          author=user_that_made_comm, post=post)
        db.add(comment)
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {e}')


# PUT A COMMENT

@router.put('/{user_id}/{post_id}/comments/{comment_id}')
async def update_comment(comment_req: CommentRequest,
                         user_id: int = Path(gt=0),
                         post_id: int = Path(gt=0),
                         comment_id: int = Path(gt=0),
                         user_data: dict = Depends(check_jwt),
                         db: AsyncSession = Depends(get_db)):
    try:
        user_that_changed_comm = await get_user_by_id(db=db, user_id=comment_req.author_id)
        if not user_that_changed_comm:
            raise HTTPException(status_code=404, detail='User not found')

        if user_that_changed_comm.username != user_data['username']:
            raise HTTPException(status_code=403, detail='Permission denied')

        comment_res = await db.execute(select(Comment).where(Comment.id == comment_id))
        comment = comment_res.scalars().first()
        if not comment:
            raise HTTPException(status_code=404, detail='Comment not found')

        comment.body = comment_req.body
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {e}')


# DELETE COMMENT

@router.delete('/{user_id}/{post_id}/comments/{comment_id}')
async def delete_comment(user_id: int = Path(gt=0),
                         post_id: int = Path(gt=0),
                         comment_id: int = Path(gt=0),
                         user_data: dict = Depends(check_jwt),
                         db: AsyncSession = Depends(get_db)):

    try:
        comment_to_delete = await db.execute(
            select(Comment).filter(Comment.id == comment_id, Comment.post_id == post_id))
        if not comment_to_delete:
            raise HTTPException(status_code=404, detail='Didnt find such comment, sorry!')

        await db.delete(comment_to_delete)
        await db.commit()

    except ConnectionError as conn_e:
        raise HTTPException(status_code=503, detail=f'Database connection error: {conn_e}')

    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {e}')

