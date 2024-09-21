import pika
import json
from django.conf import settings


def send_book_message(method, body):
    # Set up a connection to RabbitMQ
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

    # Declare a queue (create it if it doesn't exist)
    channel.queue_declare(queue=method, durable=True)

    # Publish the book data message to the queue
    message = json.dumps(body)
    channel.basic_publish(
        exchange='',
        routing_key=method,
        body=message,
        properties=pika.BasicProperties(
            method,
            delivery_mode=2,  # Make the message persistent
        )
    )

    # Close the connection
    connection.close()
