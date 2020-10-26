from django.core.validators import MinLengthValidator
from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=300, validators=[MinLengthValidator(5)])
    date_event = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    category = models.CharField(max_length=50)
    price = models.DecimalField(blank=False, max_digits=8, decimal_places=2)
    qty = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
