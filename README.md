# Deploying a Dockerized Django Rest Framework API to AWS EC2 Instance with Nginx and Gunicorn
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

Execute
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

## Celery
Celery is a powerful asynchronous task queue that can be used with Django to run tasks in the background, outside of the request-response cycle. This allows you to offload time-consuming tasks such as sending emails or processing large files to separate worker processes, freeing up your web server to handle incoming requests more efficiently.


To get started with Celery in your Django project, you'll need to follow these steps:

1) add celery, django-celery-beat to requirements.txt

2) Add the following settings to your Django settings.py file:
```python
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = os.getenv("REDIS_BACKEND")
CELERY_BEAT_SCHEDULE_FILENAME = '/app/celerybeat-schedule'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
```
3) To schedule tasks, add CELERY_BEAT_SCHEDULE to settings.py
```python
CELERY_BEAT_SCHEDULE = {
    "some_task": {
        "task": "your_app.tasks.some_task",
        "schedule": crontab(minute="*"),
    },
}
```

## Production
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
## Deployment
Follow the steps below to deploy the Django Rest Framework API to an AWS EC2 instance:
1. Create an AWS account <br>
If you don't have one already, create an AWS account by visiting https://aws.amazon.com/ and clicking on "Create an AWS Account".
2. Create an Amazon Linux EC2 instance <br>
Once you have created an AWS account, create an Amazon Linux EC2 instance by following these steps:
- Login to the AWS console.
- Click on the "EC2" service.
- Click on the "Launch Instance" button.
- Select the "Amazon Linux 2 AMI" instance type.
- Select an instance type, such as "t2.micro".
- Click on "Review and Launch" button.
- Click on "Launch" button.
3. Create a .pem file and connect via SSH <br>
- Create a .pem file and connect to the EC2 instance via SSH by following these steps:
- In the AWS console, select the EC2 instance that you just created.
- Click on the "Connect" button.
- Follow the instructions to create a new key pair or use an existing one.
- Click on "Download Remote Access Key" to download the .pem file.
- Change the permissions of the .pem file by running chmod 400 /path/to/your-key-pair.pem.
- Connect to the EC2 instance via SSH by running ssh -i /path/to/your-key-pair.pem ec2-user@ec2-xx-xx-xx-xx.compute-1.amazonaws.com.
4. Install Docker and Docker Compose <br>
Install Docker and Docker Compose on the EC2 instance by running the following commands:
```bash
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
sudo chkconfig docker on
sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
5. Push the Docker image to Docker Hub <br>
Push the Docker image to Docker Hub by following these steps:
- Login to Docker Hub by running docker login.
- Tag the Docker image by running docker tag <image-id> <username>/<repository>:<tag>.
- Push the Docker image by running docker push <username>/<repository>:<tag>.
6. Pull the Docker image and run <br>
Pull the Docker image from Docker Hub and run it on the EC2 instance by following these steps:
- SSH into the EC2 instance.
- Create a docker-compose.yml file with the appropriate configuration.
- Run the Docker containers by running docker-compose up -d.

And that's it! Your Django Rest Framework API should now be running on the AWS EC2 instance.

