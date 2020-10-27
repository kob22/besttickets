from rest_framework import serializers

from . import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ("id", "name", "date_event")


class TicketTypeSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False
    )

    class Meta:
        model = models.TicketType
        fields = ("id", "event", "category", "price", "qty")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ("id", "type", "status", "order")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ("id", "total", "paid", "paid_date", "created_at", "expired_at")


class CartSerializer(serializers.Serializer):
    ticket_type = serializers.PrimaryKeyRelatedField(
        queryset=models.TicketType.objects.all()
    )
    quantity = serializers.IntegerField()

    def validate(self, data):
        if (data["ticket_type"].Tickets.count() + data["quantity"]) <= data[
            "ticket_type"
        ].qty:
            return data
        else:
            raise serializers.ValidationError("Not enough tickets")
