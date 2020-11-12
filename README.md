[![codecov](https://codecov.io/gh/kob22/besttickets/branch/develop/graph/badge.svg)](https://codecov.io/gh/kob22/besttickets)
# REST API ticket selling platform

DRF + postgresql + docker
## Install

    docker-compose build

## Run the app

    docker-compose up

## Run the tests

    ./manage.py test
    
## Swagger documentation
    http://0.0.0.0:8000/swagger/
# REST API

The REST API besttickets is described below.

## Events

### Get list of events

`GET /events/`

    curl -i -H 'Accept: application/json' http://0.0.0.0:8000/events/
    
### Get list of events with tickets

`GET /events/?tickets`

    curl -i -H 'Accept: application/json' http://0.0.0.0:8000/events/?tickets

### Get single event with/without tickets

`GET /events/:event_id/?tickets`

    curl -i -H 'Accept: application/json' http://0.0.0.0:8000/events/:event_id/?tickets

### Get a list of tickets

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