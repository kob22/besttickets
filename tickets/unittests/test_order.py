import datetime
from decimal import Decimal
from unittest import mock

import pytz
from django.core.exceptions import ValidationError
from django.db.utils import DataError
from django.test import TestCase

from besttickets.settings import REST_FRAMEWORK
from tickets.models import Order
from tickets.serializers import EventSerializer


class OrderModelTest(TestCase):
    def test_create_order_model(self):
        date_to_mock = datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch(
            "django.utils.timezone.now", mock.Mock(return_value=date_to_mock)
        ):
            order = Order(total=1000)
            order.save()
        order.refresh_from_db()
        self.assertEqual(order.created_at, date_to_mock)
        # self.assertEqual(order.expired_at, date_to_mock + datetime.timedelta(minutes=15) )
        self.assertEqual(order.total, Decimal("1000.00"))
        self.assertEqual(order.paid, "N")
        self.assertEqual(order.paid_date, None)
