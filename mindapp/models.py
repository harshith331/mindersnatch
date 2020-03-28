from django.db import models
from datetime import datetime
# Create your models here.
class Config(models.Model):
    start_time = models.DateTimeField(default=datetime.now)
    end_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return "Start and End Time"