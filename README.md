
# Cowrywise Backend Assessment

This repository is a backend assessment project aimed at managing book borrowing and lending between users, interacting with an admin API, and implementing RabbitMQ for message brokering between services. The project is split into two parts: an **Admin API** running on Docker, and a **Frontend API** managing the book lending and borrowing system.

## Features

- **Admin API**: 
  - Create, update, delete books.
  - Health check endpoint.
- **Frontend API**:
  - Register and manage book users.
  - Borrow and return books.
  - API endpoints to handle borrowing and returning books based on availability.
  - Consumes RabbitMQ messages from the Admin API regarding book changes.
- **Message Brokering**: 
  - RabbitMQ is used to communicate book creation, updates, and deletions between the Admin and Frontend APIs.
- **Database**:
  - Admin API uses PostgreSQL (Dockerized).
  - Frontend API uses SQLite for simplicity.

## Requirements

- Docker
- Python 3.x
- RabbitMQ
- Elasticsearch (for search functionality)

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/Blazskills/cowrywise-backend-assessment.git
cd cowrywise-backend-assessment
```

### 2. Setting Up the Admin API

The Admin API runs in Docker using a PostgreSQL database, RabbitMQ, and Elasticsearch.

To start the Docker containers, navigate to the `admin_api` directory and run:

```bash
docker compose -f local.yml up --build -d --remove-orphans
```

The Admin API should now be running, including RabbitMQ and Elasticsearch services.

You can check the RabbitMQ management console via [http://localhost:15672](http://localhost:15672) with default credentials (`guest`/`guest`), or those specified in your Docker Compose environment variables.

### 3. Setting Up the Frontend API

#### Virtual Environment
To set up the virtual environment for the Frontend API, run:

```bash
python -m venv venv
source venv/bin/activate
pip install -r frontend_api/requirements.local.txt
```

#### Running the Frontend API
Ensure your virtual environment is activated, then run the server:

```bash
python manage.py migrate
python manage.py runserver
```

The Frontend API should now be running on [http://localhost:8000](http://localhost:8000).

### 4. Bulk Create Book Users

There is a management command to bulk create `BookUser` records. You can run it with:

```bash
python manage.py create_bulk_bookusers
```

### 5. Running the Consumer to Listen to RabbitMQ

The consumer listens for messages from the RabbitMQ broker and updates the book records based on the messages received (e.g., book creation, deletion, and updates). 

To start the consumer process, run:

```bash
python manage.py consume_books
```

This command will continuously listen for messages from the Admin API.

### 6. Elasticsearch Setup

Elasticsearch is used for the Admin API to handle advanced search queries (e.g., full-text search on book fields).

To set up and run Elasticsearch, ensure it's included in your Docker Compose setup for the Admin API. You can access Elasticsearch at [http://localhost:9200](http://localhost:9200).

### 7. Postman Collection

The Postman collection provided for this project can be imported to test API endpoints. You can find it [here](https://drive.google.com/file/d/1DaJaFWOSbb1OP-S0IpXzJo0BN6YonO75/view?usp=sharing).

### Key API Endpoints:

#### Admin API

- **Create a Book**: `POST /api/v1/admin/books/`
- **Update a Book**: `PUT /api/v1/admin/books/{book_id}/`
- **Delete a Book**: `DELETE /api/v1/admin/books/{book_id}/`

#### Frontend API

- **Get All Users**: `GET /api/v1/frontend/users/`
- **Borrow a Book**: `POST /api/v1/frontend/borrow/`
- **Return a Book**: `POST /api/v1/frontend/return/`

## RabbitMQ Integration

Messages regarding book creation, updates, and deletions are published by the Admin API to RabbitMQ queues (`book_queue`, `book_queue_update`, `book_queue_delete`), and are consumed by the Frontend API.

### RabbitMQ Consumer Functionality

- On book creation: a new book is added to the frontend database.
- On book update: the corresponding book in the frontend database is updated.
- On book deletion: if the book is borrowed and not returned, it is marked as returned before deletion from the frontend database.

## Error Handling

- Borrowing the same book twice is restricted for a single user.
- Handling cases where a borrowed book is deleted or marked unavailable by the Admin API.

## Running Tests

To run tests:

```bash
python manage.py test
```

## Conclusion

This backend project demonstrates integrating microservices with RabbitMQ for messaging and Docker for managing different services like Elasticsearch and RabbitMQ. The Admin and Frontend APIs communicate seamlessly, ensuring book borrowing and lending operations are synchronized between them.