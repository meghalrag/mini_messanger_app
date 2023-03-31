from app.models import User, Post
from app.schema import UserLoginSchema


def insert_user(db, data: dict):
    db_user = User(**data)
    db.session.add(db_user)
    db.session.commit()
    return db_user


def insert_post(db, data_dict: dict):
    db_post = Post(**data_dict)
    db.session.add(db_post)
    db.session.commit()
    return db_post


def get_all_post(db):
    return db.session.query(Post).all()

def get_post_of_user(db, user_id):
    return db.session.query(Post).filter(Post.user_id == user_id)

def get_post_by_id(db, id):
    return db.session.query(Post).filter(Post.id == id)

def get_user_by_email(db, email:str):
    return db.session.query(User).filter(User.email == email).first()

def get_user_by_id(db, id:int):
    return db.session.query(User).filter(User.id == id).first()


def check_user(db, data: UserLoginSchema):
    user = db.session.query(User).filter(User.email==data.email, User.password==data.password)
    for _ in user:
        return True
    else:
        return False