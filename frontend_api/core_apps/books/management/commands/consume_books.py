# your_app/management/commands/consume_books.py

from django.core.management.base import BaseCommand

from consumer import consume_book_events


class Command(BaseCommand):
    help = 'Consume book creation events from RabbitMQ'

    def handle(self, *args, **kwargs):
        consume_book_events()
