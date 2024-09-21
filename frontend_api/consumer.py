import json
import pika
from django.conf import settings

from core_apps.books.models import Book


def consume_book_events():
    # Set up connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            credentials=pika.PlainCredentials(
                username=settings.RABBITMQ_USER,
                password=settings.RABBITMQ_PASSWORD
            )
        )
    )

    channel = connection.channel()

    # Declare the queues you're consuming from
    channel.queue_declare(queue='book_queue', durable=True)
    channel.queue_declare(queue='book_queue_update', durable=True)
    channel.queue_declare(queue='book_queue_delete', durable=True)

    # Define the callback function to handle book creation
    def handle_book_creation(ch, method, properties, body):
        book_data = json.loads(body)
        print(book_data)
        Book.objects.create(
            id=book_data['id'],
            title=book_data['title'],
            author=book_data['author'],
            publisher=book_data['publisher'],
            category=book_data['category'],
            is_available=book_data['is_available']
        )
        print(f"Book created: {book_data['title']}")

    # Define the callback function to handle book updates
    def handle_book_update(ch, method, properties, body):
        book_data = json.loads(body)
        book = Book.objects.get(pk=book_data['id'])
        book.title = book_data['title']
        book.author = book_data['author']
        book.publisher = book_data['publisher']
        book.category = book_data['category']
        book.is_available = book_data['is_available']
        book.save()
        print(f"Book updated: {book_data['title']}")

    # Define the callback function to handle book deletion
    def handle_book_deletion(ch, method, properties, body):
        book_data = json.loads(body)
        book = Book.objects.get(pk=book_data['id'])
        book.delete()
        print(f"Book deleted with ID: {book_data['id']}")

    # Consume messages from the book creation queue
    channel.basic_consume(
        queue='book_queue',
        on_message_callback=handle_book_creation,
        auto_ack=True
    )

    # Consume messages from the book update queue
    channel.basic_consume(
        queue='book_queue_update',
        on_message_callback=handle_book_update,
        auto_ack=True
    )

    # Consume messages from the book deletion queue
    channel.basic_consume(
        queue='book_queue_delete',
        on_message_callback=handle_book_deletion,
        auto_ack=True
    )

    print('Waiting for messages...')
    channel.start_consuming()
