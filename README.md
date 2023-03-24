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
