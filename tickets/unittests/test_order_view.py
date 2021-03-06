import json
import random
from concurrent import futures
from decimal import Decimal

from django.http import QueryDict
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory

from tickets.models import Order, Ticket, TicketType
from tickets.views import OrderListView


class OrderViewListTest(TestCase):

    fixtures = [
        "tickets/unittests/fixtures/events.json",
        "tickets/unittests/fixtures/two_events_four_tickets.json",
    ]

    def setUp(self) -> None:
        self.cart = [
            {"ticket_type": 1, "quantity": 2},
            {"ticket_type": 2, "quantity": 3},
        ]

    def test_make_simple_order(self):

        factory = APIRequestFactory()
        order_view = OrderListView.as_view()
        request = factory.post(
            reverse("order-list"),
            json.dumps(self.cart),
            content_type="application/json",
        )
        response = order_view(request)
        response.render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertCountEqual(
            json.loads(response.content).keys(),
            ["id", "total", "paid", "paid_date", "created_at", "expired_at"],
        )
        self.assertEqual(response["content-type"], "application/json")

    def test_make_order_check_total(self):
        factory = APIRequestFactory()
        order_view = OrderListView.as_view()
        request = factory.post(
            reverse("order-list"),
            json.dumps(self.cart),
            content_type="application/json",
        )
        response = order_view(request)

        total = Decimal(0)
        for item in self.cart:
            total += (
                TicketType.objects.get(pk=item["ticket_type"]).price * item["quantity"]
            )

    def test_make_order_check_if_creates_tickets(self):
        factory = APIRequestFactory()
        order_view = OrderListView.as_view()
        request = factory.post(
            reverse("order-list"),
            json.dumps(self.cart),
            content_type="application/json",
        )
        response = order_view(request)

        for item in self.cart:
            self.assertEqual(
                Ticket.objects.filter(type=item["ticket_type"]).count(),
                item["quantity"],
            )

    def test_order_with_invalid_cart(self):
        cart = [
            {"tickettype": 6, "qty": 3},
            {"ticket_type": 88, "quantity": 2},
        ]

        factory = APIRequestFactory()
        order_view = OrderListView.as_view()
        request = factory.post(
            reverse("order-list"),
            json.dumps(cart),
            content_type="application/json",
        )
        response = order_view(request)
        response.render()

        self.assertEqual(Order.objects.all().count(), 0)
        self.assertEqual(Ticket.objects.all().count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["content-type"], "application/json")

    def test_order_with_zero_quantity(self):
        cart = [
            {"ticket_type": 1, "quantity": 2},
            {"ticket_type": 2, "quantity": 0},
        ]

        factory = APIRequestFactory()
        order_view = OrderListView.as_view()
        request = factory.post(
            reverse("order-list"),
            json.dumps(cart),
            content_type="application/json",
        )
        response = order_view(request)
        response.render()

        self.assertEqual(Order.objects.all().count(), 0)
        self.assertEqual(Ticket.objects.all().count(), 0)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response["content-type"], "application/json")


# class OrderRaceTest(TestCase):
#
#     fixtures = [
#             "tickets/unittests/fixtures/events.json",
#             "tickets/unittests/fixtures/two_events_four_tickets.json",
#         ]
#     def test_check_race_condition_if_not_creates_too_much_tickets(self):
#
#         carts = []
#         total_tickets = 0
#         for i in range(20):
#             ticket_by_round = random.randint(1,10)
#             total_tickets+=ticket_by_round
#             carts.append([{"ticket_type": 1, "quantity": ticket_by_round}, {"ticket_type": 2, "quantity": random.randint(1,2)}])
#         executor =futures.ProcessPoolExecutor(max_workers=2)
#         results= [executor.submit(make_order_requests, cart) for cart in carts]
#         executor.shutdown(wait=True)
#
#
#
# def make_order_requests(cart):
#     factory = APIRequestFactory()
#     order_view = OrderListView.as_view()
#     request = factory.post(
#         reverse("order-list"), json.dumps(cart), content_type="application/json"
#     )
#     response = order_view(request)
#     response.render()
#     return response.content
