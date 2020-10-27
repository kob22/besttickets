from django.test import TestCase
from rest_framework.exceptions import ValidationError

from tickets.models import Order, Ticket, TicketType
from tickets.serializers import CartSerializer


class CartSerializerTest(TestCase):
    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def test_ticket_quantity_validation_cart_serializer(self):
        cart_data = [
            {"ticket_type": 1, "quantity": 2},
            {"ticket_type": 2, "quantity": 3},
            {"ticket_type": 3, "quantity": 1},
        ]
        cart = CartSerializer(data=cart_data, many=True)
        self.assertTrue(cart.is_valid(raise_exception=True))

    def test_validation_cart_unexisting_ticket_type(self):
        cart_data = [
            {"ticket_type": 1, "quantity": 2},
            {"ticket_type": 22, "quantity": 3},
            {"ticket_type": 3, "quantity": 1},
        ]
        cart = CartSerializer(data=cart_data, many=True)
        with self.assertRaises(ValidationError):
            cart.is_valid(raise_exception=True)

    def test_validation_cart_not_enough_qty(self):
        cart_data = [
            {"ticket_type": 1, "quantity": 1500},
            {"ticket_type": 3, "quantity": 3},
        ]
        cart = CartSerializer(data=cart_data, many=True)
        with self.assertRaises(ValidationError):
            cart.is_valid(raise_exception=True)

    def test_validation_cart_not_enough_qty_with_existing_tickets_inDB(self):
        ticket_type = TicketType.objects.get(pk=1)
        order = Order(total=10)
        order.save()

        # create fake tickets
        for _ in range(ticket_type.qty - 3):
            Ticket.objects.create(type=ticket_type, order=order)

        cart_data = [
            {"ticket_type": 1, "quantity": 5},
            {"ticket_type": 3, "quantity": 3},
        ]
        cart = CartSerializer(data=cart_data, many=True)
        with self.assertRaises(ValidationError):
            cart.is_valid(raise_exception=True)
