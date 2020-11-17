from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
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

    def list(self, request):
        queryset = Event.objects.all()
        if request.GET.get("tickets", None) is not None:
            nested_tickets = True
        else:
            nested_tickets = False
        serializer = EventSerializer(queryset, many=True, nested=nested_tickets)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Event.objects.all()
        if request.GET.get("tickets", None) is not None:
            nested_tickets = True
        else:
            nested_tickets = False
        event = get_object_or_404(queryset, pk=pk)
        serializer = EventSerializer(event, nested=nested_tickets)
        return Response(serializer.data)


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


class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer
    filterset_fields = ("event",)


class OrderListView(APIView):
    """
    create a new order.
    """

    def post(self, request):
        cart = CartSerializer(data=request.data, many=True)
        # if cart is correct, create order, tickets and count total sum for order
        if cart.is_valid(raise_exception=True) and len(cart.validated_data):
            # make order and reserve tickets in transaction
            with transaction.atomic():
                order = Order()
                order.save()
                for item in cart.validated_data:
                    for _ in range(item["quantity"]):
                        order.total += item["ticket_type"].price
                        ticket = Ticket(type=item["ticket_type"], order=order)
                        ticket.save()
                order.save()
                order_serializer = OrderSerializer(instance=order)
                return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# def create_tickets(request, how_many):
#     ticket_type = TicketType.objects.get(pk=1)
#     data = [{"type": 1}, {"type": 1}, {"type": 1}]
#     ticket_serializer = TicketSerializer(data=data, many=True)
#     if ticket_serializer.is_valid():
#         with transaction.atomic():
#             ticket_serializer.save()
