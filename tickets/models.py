from django.db import models
from django.core.validators import MinLengthValidator


class Event(models.Model):
    name = models.CharField(max_length=300, validators=[MinLengthValidator(5)])
    date_event = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
