import datetime
import time
from decimal import Decimal
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from rest_framework.exceptions import ValidationError as ValidationErrorRF

from tickets.models import Event, TicketType
from tickets.serializers import TicketTypeSerializer


class TicketTypeModelTest(TestCase):

    fixtures = ["tickets/unittests/fixtures/events.json"]

    def test_create_ticket_type(self):
        event = Event.objects.get(id=1)
        date_to_mock = datetime.datetime(2020, 2, 5, 22, 23, 1, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            ticket_type = TicketType(
                event=event, category="VIP", price=Decimal("1999.99"), qty=500
            )
            ticket_type.save()
            ticket_type.full_clean()
        self.assertEqual(ticket_type.event, event)
        self.assertEqual(ticket_type.created_at, date_to_mock)
        self.assertEqual(ticket_type.category, "VIP")
        self.assertEqual(ticket_type.price, Decimal("1999.99"))
        self.assertEqual(ticket_type.qty, 500)

    def test_check_ticket_type_price_type(self):
        event = Event.objects.get(id=1)
        ticket_type = TicketType(event=event, category="VIP", price=1990, qty=500)
        ticket_type.save()
        ticket_type.full_clean()

        self.assertTrue(isinstance(ticket_type.price, Decimal))

    def test_create_ticket_type_without_event(self):
        ticket_type = TicketType(category="VIP", price=Decimal("1999.99"), qty=500)

        with self.assertRaises(IntegrityError):
            ticket_type.save()
            ticket_type.full_clean()

    def test_create_ticket_type_with_non_event_object(self):

        with self.assertRaises(ValueError):
            ticket_type = TicketType(
                event=55, category="VIP", price=Decimal("1999.99"), qty=500
            )

    def test_max_length_category_field(self):
        event = Event.objects.get(id=1)
        with self.assertRaises(DataError):
            ticket_type = TicketType(
                event=event, category="V" * 51, price=Decimal("1999.99"), qty=500
            )
            ticket_type.save()
            ticket_type.full_clean()

    def test_delete_event_with_ticket_types_should_raise_error(self):
        event = Event.objects.get(id=1)

        ticket_type = TicketType(
            event=event, category="VIP", price=Decimal("1999.99"), qty=500
        )
        ticket_type.save()
        with self.assertRaises(ProtectedError):
            event.delete()

    def test_check_available_tickets_with_not_sold(self):

        event = Event.objects.get(id=1)
        ticket_type = TicketType(event=event, category="VIP", price=1990, qty=500)
        ticket_type.save()
        ticket_type.full_clean()
        ticket_type.refresh_from_db()

        self.assertEqual(ticket_type.tickets_available, 500)

    def test_test_check_available_tickets_when_sold(self):

        event = Event.objects.get(id=1)
        ticket_type = TicketType(event=event, category="VIP", price=1990, qty=500)
        ticket_type.save()
        ticket_type.full_clean()
        ticket_type.refresh_from_db()
        mock_query_set = mock.MagicMock()
        with mock.patch("tickets.models.TicketType.tickets", mock_query_set):
            mock_query_set.count.return_value = 100
            self.assertEqual(ticket_type.tickets_available, 400)


class TicketSerializerTest(TestCase):

    fixtures = ["tickets/unittests/fixtures/events.json"]

    def setUp(self) -> None:

        self.event = Event.objects.get(id=1)

        self.ticket_type_attr = {
            "id": 2,
            "event": self.event,
            "category": "Premium",
            "price": Decimal("2999.99"),
            "qty": 99,
        }
        self.ticket_type_serialized = {
            "id": 2,
            "event": 1,
            "category": "Premium",
            "price": Decimal("2999.99"),
            "qty": 99,
            "tickets_available": 99,
        }
        self.ticket_type_serialized_with_out_tickets_avb = {
            "id": 2,
            "event": 1,
            "category": "Premium",
            "price": Decimal("2999.99"),
            "qty": 99,
        }
        self.ticket_type = TicketType.objects.create(**self.ticket_type_attr)
        self.ticket_type_obj_serialized = TicketTypeSerializer(
            instance=self.ticket_type
        )

    def test_check_ticket_type_price_type(self):
        self.assertTrue(
            isinstance(self.ticket_type_obj_serialized.data["price"], Decimal)
        )

    def test_ticket_type_serializer_contains_correct_data(self):
        self.assertEqual(
            self.ticket_type_obj_serialized.data, self.ticket_type_serialized
        )

    def test_create_ticket_type_from_data(self):
        self.serialized_ticket_type = TicketTypeSerializer(
            data=self.ticket_type_serialized_with_out_tickets_avb
        )
        self.assertTrue(self.serialized_ticket_type.is_valid())

    def test_create_ticket_type_from_data_with_wrong_event(self):
        ticket_type_serialized_wrong_event_id = {
            "id": 1,
            "event": 100,
            "category": "Premium",
            "price": Decimal("2999.99"),
            "qty": 99,
        }
        serialized_ticket_type_wrong_event = TicketTypeSerializer(
            data=ticket_type_serialized_wrong_event_id
        )

        with self.assertRaises(ValidationErrorRF):
            serialized_ticket_type_wrong_event.is_valid(raise_exception=True)
