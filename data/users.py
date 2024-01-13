from database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import relationship
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(autoincrement=True, index=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    posts: Mapped[relationship] = relationship('Post', back_populates='author')
    comments: Mapped[relationship] = relationship('Comment', back_populates='author')
