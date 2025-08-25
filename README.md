````markdown
# Bookstore API

A RESTful API for managing books, orders, and users built with Django REST Framework (DRF).

## Features

- User authentication (JWT / DRF token authentication)
- CRUD operations for:
  - Books
  - Authors
  - Categories
  - Orders
- Place orders with multiple items
- Update order status (admin only)
- Email notifications for order placement
- Throttling to limit API requests
- Swagger API documentation with `drf_yasg`
- Role-based access control (Admin / Regular user)


## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL / SQLite (DB configurable)
- `drf_yasg` for API documentation
- Django email backend for notifications

````
## Installation

1. Clone the repository:

```bash
git clone https://github.com/talibraath/BookStore
cd BookStore
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up `.env` file with required environment variables:

```env
SECRET_KEY=<your-django-secret-key>
DEBUG=True
EMAIL_HOST=<smtp-host>
EMAIL_PORT=<smtp-port>
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>
EMAIL_USE_TLS=True
```

5. Run migrations:

```bash
python manage.py migrate
```

6. Create superuser (admin):

```bash
python manage.py createsuperuser
```

7. Run the server:

```bash
python manage.py runserver
```

---

## API Documentation

Swagger documentation is available at:

```
http://127.0.0.1:8000/documentation/
```

## Example API Requests

## Order Flow

1. User places an order with multiple books.
2. Stock is verified before order creation.
3. Total amount is calculated automatically.
4. Email notification is sent to user and admin.
5. Admin can update the order status (`pending`, `shipped`, `delivered`, `canceled`).


## Throttling

DRF throttling is applied by default:

* Anonymous users: 20 requests/day
* Authenticated users: 50 requests/day

Custom throttling can be implemented based on user roles.


## Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Add feature"`
4. Push: `git push origin feature-name`
5. Create a pull request
