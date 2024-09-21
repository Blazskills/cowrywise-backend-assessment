import json
import pika
from django.conf import settings

from core_apps.books.models import Book, Borrow
from django.utils import timezone


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

    def handle_book_update(ch, method, properties, body):
        book_data = json.loads(body)
        book_id = book_data['id']

        # Get the book and check if it has been marked as unavailable
        if book_data['is_available'] is False:
            print("now unavailable")
            # Check if the book is currently borrowed and not returned
            borrowed_books = Borrow.objects.select_related("book_user", "book").filter(book_id=book_id, return_date__isnull=True)

            for borrow in borrowed_books:
                # Mark the book as returned
                borrow.return_date = timezone.now()
                borrow.save()
        book = Book.objects.get(pk=book_data['id'])
        book.title = book_data['title']
        book.author = book_data['author']
        book.publisher = book_data['publisher']
        book.category = book_data['category']
        book.is_available = book_data['is_available']
        book.save()
        print(f"Book updated: {book_data['title']}")

    def handle_book_deletion(ch, method, properties, body):
        book_data = json.loads(body)
        book = Book.objects.get(pk=book_data['id'])
        # Check if the book exists in borrowed records and hasn't been returned
        # This line of code useless because cascade will eventually delete all related books in borrow model.
        borrowed_books = Borrow.objects.select_related("book_user", "book").filter(book_id=book, return_date__isnull=True)

        for borrow in borrowed_books:
            # Mark the book as returned
            borrow.return_date = timezone.now()
            borrow.save()
        book.delete()
        # force book return from borrowers
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
