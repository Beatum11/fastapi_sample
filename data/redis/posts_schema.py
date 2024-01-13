from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from data.posts import Post


# Class for working with posts in redis
class PostSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        load_instance = True
