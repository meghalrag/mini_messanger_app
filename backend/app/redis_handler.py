# from dotenv import load_dotenv
# import redis
# import os


# load_dotenv()

# r = redis.Redis(
#     host=os.environ['REDIS_HOST'],
#     port=os.environ['REDIS_PORT'],
#     db=0,
#     password=os.environ['REDIS_PASSWORD'],
#     decode_responses=True,
# )


# def insert_redis(key: str, value: str = None, expiry=None, keepttl=False):
#     if keepttl:
#         return r.set(key, value, keepttl=keepttl)
#     return r.set(key, value, ex=expiry)


# def check_redis(key: str):
#     if r.get(key) is None:
#         return False
#     else:
#         return True


# def get_redis(key: str):
#     return r.get(key)


# def delete_redis(prefix_or_key: str):
#     """
#     This function is used to delete redis keys based on prefix or key
#     """
#     for key in r.scan_iter(f"{prefix_or_key}*"):
#         r.delete(key)


# def delete_redis_key(key: str):
#     """
#     This function is used to delete a specific key
#     """
#     if check_redis(key):
#         r.delete(key)
        
# if __name__ == "__main__":
#     insert_redis("123", "test redis")
#     get_redis("123")
