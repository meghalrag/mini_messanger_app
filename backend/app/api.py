# app/api.py
import os
import json
from loguru import logger
from fastapi import FastAPI, Body, Depends, Request, APIRouter
from fastapi import WebSocket, WebSocketDisconnect

from app.schema import PostSchema, UserSchema, UserLoginSchema
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import JWTBearer
import app.crud as crud
from fastapi_sqlalchemy import DBSessionMiddleware, db
from app.utils import get_requested_user, get_all_posts
from app.websocket.config import init_connection
# from app.redis_handler import get_redis


from dotenv import load_dotenv

load_dotenv('.env')

app = FastAPI()
# to avoid csrftokenError
app.add_middleware(DBSessionMiddleware, db_url=os.environ['DATABASE_URL'])

manager = init_connection()


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your blog!"}


@app.get("/api/get_all_posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def get_posts() -> dict:
    result_list = get_all_posts(db)
    return { "data": result_list }


@app.get("/api/user_post", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def get_single_post(request:Request) -> dict:
    user_obj = get_requested_user(request, db)
    posts = crud.get_post_of_user(db, user_obj.id)
    result_list = []
    for each in posts:
        temp = {}
        temp["title"] = each.title
        temp["content"] = each.content
        result_list.append(temp)
        del temp
    return { "data": result_list }
            

@app.post("/api/post", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(request:Request, post: PostSchema) -> dict:
    user_obj = get_requested_user(request, db)
    post = post.dict()
    post["user_id"] = int(user_obj.id)
    
    res = crud.insert_post(db, post)
    socket_dict = {
        "id": res.id,
        "user_id":res.user_id,
        "title": res.title,
        "content": res.content,
        "date": str(res.time_created.date()),
        "time": str(res.time_created.time()),
    }
    
    return {
        "data": "post added."
    }
   
    
@app.delete("/api/post/{id}", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def delete_post(id: int) -> dict:
    post_obj = crud.get_post_by_id(db, id)
    post_obj.delete()
    db.session.commit()
    
    return {
        "data": "post deleted."
    }
    
    
@app.post("/api/signup", tags=["user"])
async def create_user(user: UserSchema = Body(...)):
    if crud.get_user_by_email(db, user.email):
        return {
            "error": "User already exists"
        }
    else:
        crud.insert_user(db, user.dict())
        return signJWT(user.email)


@app.post("/api/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if crud.check_user(db, user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }
    

@app.get("/api/user_profile", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_login(request: Request):
    user_obj = get_requested_user(request, db)
    return user_obj.__dict__
    
    
# websocket endpoints
# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     try:
#         await manager.connect(websocket)
#         result_list = get_redis("posts")
#         await manager.send_personal_message(result_list, websocket)
#         while True:
#             logger.debug(f"socket waiting {websocket}")
#             data = await websocket.receive_text()
#             logger.debug(f"data recieved {data}")
#             logger.success(data, "=========socket=========")
#             # result_list = get_redis("posts")
#             await manager.broadcast(result_list)
#     except WebSocketDisconnect:
#         logger.warning(f"Connected client already left the chat {websocket}")
#     except Exception as err:
#         logger.error(err)
    