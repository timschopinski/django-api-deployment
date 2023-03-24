from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from app.settings import EMAIL_HOST_USER
from celery.utils.log import get_task_logger
from events.models import Event

logger = get_task_logger(__name__)


@shared_task
def send_event_email_task(email: str, event_id: int):
    try:
        event = Event.objects.get(id=event_id)
    except ObjectDoesNotExist:
        raise Exception(f'Event ID {event_id} not found')

    message = f"""
        {event.name}\n\n
        {event.description}\n
        Location: {event.location}\n
        Date: {event.datetime.date()}
        Time: {event.datetime.time()}
    """
    email_message = EmailMessage(
        'Your Event Notification',
        message,
        EMAIL_HOST_USER,
        [email],
    )
    try:
        email_message.send()
        logger.info('Email sent successfully')
    except Exception as e:
        logger.error(e)


@shared_task
def hello_world():
    logger.info('Hello World')
