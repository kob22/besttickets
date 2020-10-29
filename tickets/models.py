from datetime import timedelta

from django.core.validators import MinLengthValidator
from django.db import IntegrityError, models, transaction
from django.utils.timezone import now


class Event(models.Model):
    name = models.CharField(max_length=300, validators=[MinLengthValidator(5)])
    date_event = models.DateTimeField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


class TicketType(models.Model):
    event = models.ForeignKey(
        Event,
        related_name="TicketTypes",
        related_query_name="TicketTypes",
        on_delete=models.PROTECT,
    )
    category = models.CharField(max_length=50)
    price = models.DecimalField(blank=False, max_digits=8, decimal_places=2)
    qty = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def tickets_available(self):
        return self.qty - self.Tickets.count()


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
        related_name="Tickets",
        related_query_name="Ticket",
        on_delete=models.PROTECT,
    )
    status = models.CharField(max_length=1, blank=False, default="R")
    order = models.ForeignKey(
        Order,
        related_name="Tickets",
        related_query_name="Ticket",
        on_delete=models.PROTECT,
    )

    def save(self, *args, **kwargs):
        if self.pk:
            super().save(*args, **kwargs)
        else:

            if Ticket.objects.filter(type=self.type).count() < self.type.qty:
                super().save(*args, **kwargs)  # Call the "real" save() method.
            else:
                raise Exception("too much tickets")
