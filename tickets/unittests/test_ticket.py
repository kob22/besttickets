import datetime
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from django.db.utils import IntegrityError
from django.test import TestCase
from tickets.models import Event, Ticket


class TicketModelTest(TestCase):

    fixtures = ["tickets/unittests/fixtures/events.json"]

    def test_create_ticket(self):
        event = Event.objects.get(id=1)
        date_to_mock = datetime.datetime(2020, 2, 5, 22, 23, 1, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            ticket = Ticket(event=event, category="VIP", price=2000, qty=500)
            ticket.save()
            ticket.full_clean()
        self.assertEqual(ticket.event, event)
        self.assertEqual(ticket.created_at, date_to_mock)
        self.assertEqual(ticket.category, "VIP")
        self.assertEqual(ticket.price, 2000)
        self.assertEqual(ticket.qty, 500)

    def test_create_ticket_without_event(self):
        ticket = Ticket(category="VIP", price=2000, qty=500)

        with self.assertRaises(IntegrityError):
            ticket.save()
            ticket.full_clean()

    def test_create_ticket_with_non_event_object(self):

        with self.assertRaises(ValueError):
            ticket = Ticket(event=55, category="VIP", price=2000, qty=500)

    def test_max_length_category_field(self):
        event = Event.objects.get(id=1)
        with self.assertRaises(ValidationError):
            ticket = Ticket(event=event, category="V" * 51, price=2000, qty=500)
            ticket.save()
            ticket.full_clean()

    def test_delete_event_with_tickets_should_raise_error(self):
        event = Event.objects.get(id=1)

        ticket = Ticket(event=event, category="VIP", price=2000, qty=500)
        ticket.save()
        with self.assertRaises(ProtectedError):
            event.delete()
