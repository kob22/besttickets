from rest_framework import serializers

from . import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ("id", "name", "date_event")


class TicketSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = models.Ticket
        fields = ("id", "event", "category", "price", "qty")
