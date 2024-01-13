from fastapi import FastAPI
from routes import users_routes, auth_route, posts_route, comments_route


app = FastAPI()

app.include_router(users_routes.router)
app.include_router(auth_route.router)
app.include_router(posts_route.router)
app.include_router(comments_route.router)

