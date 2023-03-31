def format_api_res(response):
    if response.status_code == 200 and "detail" in response.json():
        return {
            "status_code": 401,
            "error": f"{response.content['detail']}"
        }
    elif response.status_code == 200:
        response = response.json()
    else:
        return {
            "status_code": response.status_code,
            "error": f"{response.content}"
        }
    return response