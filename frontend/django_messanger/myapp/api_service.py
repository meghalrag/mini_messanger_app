import requests
from django.conf import settings
from .utils import format_api_res

API_URL = settings.API_URL


def sigup_api(params:dict):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'{API_URL}/api/signup', headers=headers, json=params)
    return format_api_res(response)


def login_api(params:dict):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    response = requests.post(f'{API_URL}/api/login', headers=headers, json=params)
    return format_api_res(response)


def user_profile_api(token:str):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'{API_URL}/api/user_profile', headers=headers)
    return format_api_res(response)


def get_post_api(token:str):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.get(f'{API_URL}/api/get_all_posts', headers=headers)
    return format_api_res(response)


def add_post_api(token:str, params: dict):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.post(f'{API_URL}/api/post', headers=headers, json=params)
    return format_api_res(response)


def delete_post_api(token:str, post_id):
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    response = requests.delete(f'{API_URL}/api/post/{post_id}', headers=headers)
    return format_api_res(response)