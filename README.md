# Deploying a Dockerized Django Rest Framework API to Digital Ocean Droplet with Nginx and Gunicorn
This guide will walk you through the process of deploying a dockerized multicontainer Django Rest Framework API built with Django, Postgres, Redis, Celery, and Celery Beat to a Digital Ocean Droplet using Nginx and Gunicorn.

## Description
The app allows users to create events and schedule notifications to be sent via Celery at a specified time.



## Prerequisites
Before you begin, make sure you have the following:

- A Digital Ocean account
- A Droplet running Ubuntu 20.04
- Docker and Docker Compose installed on your Droplet


## Setup
Clone this repository
- fill in the appropriate environment variables in .env
- Build the Docker images by running docker-compose build.
- Start the containers by running docker-compose up.
- Once the containers are running, create a superuser by running docker-compose run app python manage.py createsuperuser.
- Visit http://<your-host>:8000/swagger/ to view the API documentation.
### CODE
```yaml
docker-compose build
docker-compose up
docker-compose run --rm app sh -c "python manage.py makemigrations"
docker-compose run --rm app sh -c "python manage.py migrate"
docker-compose run --rm app sh -c "python manage.py createsuperuser"
```

## API Endpoints
- GET /events/: Get a list of all events.
- POST /events/: Create a new event.
- GET /events/{id}/: Get a single event by ID.
- PUT /events/{id}/: Update an event by ID.
- DELETE /events/{id}/: Delete an event by ID.
- POST /events/notification/: Create a notification.

## Deployment
To deploy the app to a production environment, you'll need to use the docker-compose.prod.yaml file and an Nginx configuration.
The docker-compose.prod.yaml file builds and runs the production version of the application. It is similar to the development version with some important differences, such as the removal of the volumes section, since we won't be using mounted volumes in production, and the addition of an env_file section, which loads the production environment variables from the .env_prod file. Here is the content of the docker-compose.prod.yaml file: 

```yaml
version: "3"

services:

  app:
    build:
      context: .
      dockerfile: Dockerfile.prod
    restart: always
    expose:
      - 8000
    volumes:
      - static_volume:/vol/web/static
      - media_volume:/vol/web/media
    env_file:
      - app/app/.env_prod
    depends_on:
      - redis
      - db

  db:
    restart: always
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - app/app/.env_prod

  redis:
    image: 'redis:7.0.8'

  celery:
    restart: always
    build: .
    command: celery -A app worker -l info
    volumes:
      - ./app:/app
    env_file:
      - app/app/.env_prod
    depends_on:
      - redis
      - db

  celery-beat:
    restart: always
    build: .
    command: celery -A app beat -l info
    volumes:
      - ./app:/app
    env_file:
      - app/app/.env_prod
    depends_on:
      - redis
      - db

  nginx:
    build: ./nginx
    restart: always
    ports:
      - "80:80"
    volumes:
      - static_volume:/vol/web/static
      - media_volume:/vol/web/media
    depends_on:
      - app

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## Nginx Configuration

Nginx is used as a reverse proxy to route incoming requests to the appropriate Docker container. We need to create an Nginx configuration file to define the server block and the upstream server. Here is the content of the nginx.conf file:
````bash
# nginx/nginx.conf

upstream web_app {
    server app:8000;
}

server {
    listen 80;

    location /static/ {
        alias /vol/web/static/;
    }

    location /media/ {
        alias /vol/web/media/;
    }

    location / {
        proxy_pass http://web_app;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}

````

## Deployment Steps
To deploy the application, follow these steps:

- SSH into the Droplet using your Digital Ocean account and clone the repository.
- Create a .env_prod file and fill in the required environment variables.
- Run docker-compose -f docker-compose.prod.yaml up -d to start the production containers in detached mode.
- Run docker-compose -f docker-compose.prod.yaml run --rm app python manage.py migrate to apply the database migrations.
- Create a superuser by running docker-compose -f docker-compose.prod.yaml run --rm app python manage.py createsuperuser.
- Visit the Droplet's IP address in a web browser to verify that the application is running.
- 
And that's it! You have successfully deployed a Dockerized Django Rest Framework API to a Digital Ocean Droplet using Nginx and Gunicorn.