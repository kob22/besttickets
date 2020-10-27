from django.db import transaction
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Event, Order, Ticket, TicketType
from .serializers import (
    CartSerializer,
    EventSerializer,
    OrderSerializer,
    TicketSerializer,
    TicketTypeSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


# I was thinking about url structure for ticket lists, /events/:event_id/tickets vs /tickets, I chose the first one
# and overwrites event_id from json if exists


class TicketTypeListView(APIView):
    """
    List all tickets, or create a new ticket for Event.
    """

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise Http404

        tickets_type = TicketType.objects.filter(event=event)
        serializer = TicketTypeSerializer(tickets_type, many=True)
        return Response(serializer.data)

    def post(self, request, event_id):
        data = request.data.dict()

        # method takes event_id from url
        data["event"] = event_id
        serializer = TicketTypeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# For ticket details I chose url /tickets/:ticket_id, because event_id is not needed to manage the ticket
class TicketTypeDetailView(APIView):
    """
    Retrieve, update or delete a ticket instance for Event.
    """

    def get_object(self, ticket_type_id):
        try:
            return TicketType.objects.get(pk=ticket_type_id)
        except TicketType.DoesNotExist:
            raise Http404

    def get(self, request, ticket_type_id):
        ticket_type = self.get_object(ticket_type_id)
        serializer = TicketTypeSerializer(ticket_type)
        return Response(serializer.data)

    def put(self, request, ticket_type_id):
        ticket_type = self.get_object(ticket_type_id)
        serializer = TicketTypeSerializer(ticket_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticket_type_id):
        ticket_type = self.get_object(ticket_type_id)
        ticket_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderListView(APIView):
    """
    create a new order.
    """

    def post(self, request):
        # make order and reserve tickets in transaction
        with transaction.atomic():
            order = Order()
            order.save()
            # make cart from json
            cart = CartSerializer(data=request.data, many=True)
            if cart.is_valid(raise_exception=True):
                # if cart is correct, create tickets and count total sum for order
                for item in cart.validated_data:
                    for _ in range(item["quantity"]):
                        order.total += item["ticket_type"].price
                        ticket = Ticket(type=item["ticket_type"], order=order)
                        ticket.save()
            order.save()
        order_serializer = OrderSerializer(instance=order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


# def create_tickets(request, how_many):
#     ticket_type = TicketType.objects.get(pk=1)
#     data = [{"type": 1}, {"type": 1}, {"type": 1}]
#     ticket_serializer = TicketSerializer(data=data, many=True)
#     if ticket_serializer.is_valid():
#         with transaction.atomic():
#             ticket_serializer.save()
