import datetime
import time
from decimal import Decimal
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError as ValidationErrorRF

from tickets.models import Event, Order, Ticket, TicketType
from tickets.serializers import CartSerializer, TicketSerializer, TicketTypeSerializer


class TicketViewTest(TestCase):

    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    # def test_create_ticket(self):
    #     ticket_type = TicketType.objects.get(pk=1)
    #     order = Order(total=200)
    #     order.save()
    #     for x in range(200):
    #         a = Ticket(type=ticket_type, order=order)
    #         a.save()
    #         a.full_clean()


    # def test_serializer(self):
    #
    #     order = Order(total=200)
    #     order.save()
    #     data = [{'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}, {'type': 1, 'order': order.pk}]
    #     with self.assertRaises(Exception):
    #         for i in range(75):
    #                 with transaction.atomic():
    #                     serializer = TicketSerializer(data=data, many=True)
    #                     serializer.is_valid()
    #                     serializer.save()
    #


    # def test_cart(self):
    #
    #     d = [{'ticket_type': 1, 'quantity': 30}, {'ticket_type':1, 'quantity': 5}]
    #     c = CartSerializer(data=d, many=True)
    #     c.is_valid(raise_exception=True)
    #
    #     for k in c.validated_data:
    #
    #     c.save(order='saf')
