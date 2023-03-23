from django.db import models

# Create your models here.


class Event(models.Model):

    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=100)
    datetime = models.DateTimeField()
