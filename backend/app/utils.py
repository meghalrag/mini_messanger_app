import json
from app.auth.auth_handler import decodeJWT
from app.crud import get_user_by_email
import app.crud as crud
# from app.redis_handler import insert_redis, delete_redis
from loguru import logger

def get_requested_user(request, db):
    token = request.headers["Authorization"].split(" ")[1]
    user_email = decodeJWT(token)["user_id"]
    return get_user_by_email(db, user_email)


def get_all_posts(db):
    posts = crud.get_all_post(db)
    result_list = []
    for each in posts:
        temp = {}
        temp["id"] = each.id
        temp["title"] = each.title
        temp["content"] = each.content
        temp["user_id"] = each.user_id
        temp["date"] = str(each.time_created.date())
        temp["time"] = str(each.time_created.time())
        temp["email"] = crud.get_user_by_id(db, each.user_id).email
        result_list.append(temp)
        del temp
    logger.warning(len(result_list))
    result_list = sorted(result_list, key=lambda k: k['id'], reverse=True) 
    #updated posts in redis
    # delete_redis("posts")
    # insert_redis("posts", json.dumps(result_list))
    return result_list


# @contextmanager
# def session_scope():
#     connectable = engine.execution_options(schema_translate_map=schema_translate_map)
#     con_loc, meta_loc = connect(db_user, db_pass, db_instance, 'localhost')
#     db = Session(autocommit=False, autoflush=False, bind=connectable)
#     yield db

#     """Provide a transactional scope around a series of operations."""
#     session = Session()
#     try:
#         yield session
#         session.commit()
#     except:
#         session.rollback()
#         raise
    