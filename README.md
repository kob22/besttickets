# REST API ticket selling platform

DRF + postgresql + docker
## Install

    docker-compose build

## Run the app

    docker-compose up

## Run the tests

    ./manage.py test

# REST API

The REST API besttickets is described below.

## Get list of events

### Request

`GET /events/`

    curl -i -H 'Accept: application/json' http://0.0.0.0:8000/events/

## Get a list of tickets

### Request

`GET /events/:event_id/tickets/`

    curl -i -H 'Accept: application/json' http://0.0.0.0:8000/events/1/tickets/

## Make an order for tickets

### Request

`POST /orders/`

    [
            {"ticket_type": 1, "quantity": 2},
            {"ticket_type": 2, "quantity": 3},
    ]
Where ticket_type is ID from a list of tickets, quantity is the number of ordered tickets.