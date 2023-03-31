## Setup Guide:

### Step 1
    goto the path "MINI_MESSANGER_APP/backend" and create a new virtual environment
### Step 2
    install the requirements using the following cmd:
        `pip install -r requirement.txt`

### Step 3
    create a file .env in the path MINI_MESSANGER_APP/backend and add the env variables from .env.example

### Step 4
    create a new database messanger in the postgres db

### Step 5
#### make migrations
    `
    1.alembic revision --autogenerate -m "Message"
    2.alembic upgrade head
    `
### Step 6
#### Run the application

backend:
    open the terminal in mini_messanger/backend and run the following cmd:
        `python main.py`

frontend:
    open the rerminal in mini_messanger_app\frontend\django_messanger and run the following cmd:
        `python maanage.py runserver`

All set to go😎

### Key Notes:
    1. You can see the Swagger docs for the api endpoints at [http:127.0.0.1:8081/docs](http:127.0.0.1:8081/docs)
    2. To get the frontend run goto the url [http:127.0.0.1:8000](http:127.0.0.1:8000)
