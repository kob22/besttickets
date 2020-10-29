import json
import random
import time

from locust import HttpUser, between, task


class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task(3)
    def make_order(self):
        ticket_by_round = random.randint(1, 10)

        cart = [
            {"ticket_type": 1, "quantity": ticket_by_round},
            {"ticket_type": 2, "quantity": random.randint(1, 2)},
        ]
        self.client.post("orders/", json=cart)
