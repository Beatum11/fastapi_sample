from sqlalchemy.orm import Mapped, mapped_column
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    title: Mapped[str] = mapped_column()
    body: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    author: Mapped[relationship] = relationship('User', back_populates='posts')
    comments: Mapped[relationship] = relationship('Comment', back_populates='author')