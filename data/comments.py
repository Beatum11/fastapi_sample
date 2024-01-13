from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from datetime import datetime


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(index=True, autoincrement=True, primary_key=True)
    body: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(default=None)
    author_id: Mapped[int] = mapped_column()
    author: Mapped[relationship] = relationship('User', back_populates='comments')
    post_id: Mapped[int] = mapped_column()
    post: Mapped[relationship] = relationship('Post', back_populates='comments')
