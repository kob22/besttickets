from datetime import timedelta

from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.timezone import now


class Event(models.Model):
    name = models.CharField(max_length=300, validators=[MinLengthValidator(5)])
    date_event = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class TicketType(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="ticket_types",
        related_query_name="ticket_types",
        on_delete=models.PROTECT,
    )
    category = models.CharField(max_length=50)
    price = models.DecimalField(blank=False, max_digits=8, decimal_places=2)
    qty = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tickets_available(self):
        return self.qty - self.tickets.count()


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    total = models.DecimalField(blank=False, default=0, max_digits=8, decimal_places=2)
    paid = models.CharField(max_length=1, default="N")
    paid_date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        d = timedelta(minutes=15)

        if not self.id:
            self.expired_at = now() + d
            super().save(*args, **kwargs)


class Ticket(models.Model):
    type = models.ForeignKey(
        TicketType,
        related_name="tickets",
        related_query_name="ticket",
        on_delete=models.PROTECT,
    )
    status = models.CharField(max_length=1, blank=False, default="R")
    order = models.ForeignKey(
        Order,
        related_name="tickets",
        related_query_name="ticket",
        on_delete=models.PROTECT,
    )

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
        else:
            if Ticket.objects.filter(type=self.type).count() < self.type.qty:
                super().save(*args, **kwargs)
            else:
                raise Exception("No enough tickets")
