# Bookstore API

A RESTful API for managing books, orders, and users built with **Django REST Framework (DRF)**.  
Supports **JWT authentication**, **role-based access control**, **Redis caching**, and **PostgreSQL** for production.

---

## Features

- User authentication (JWT / DRF token authentication)
- CRUD operations:
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
- Dockerized for local development & production
- Supports Redis for caching & async tasks

---

## Tech Stack

- Python 3.12
- Django 5.2
- Django REST Framework
- PostgreSQL (production) / SQLite (development)
- Redis (caching, async tasks)
- `drf_yasg` for API documentation
- Docker & Docker Compose
- Django email backend for notifications

---

## Installation (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/talibraath/BookStore
cd BookStore
```

### 2. Create `.env` file

```env
SECRET_KEY=<your-django-secret-key>
DEBUG=True
DATABASE_URL=postgres://user:password@db:5432/bookstore
REDIS_URL=redis://redis:6379/0
EMAIL_HOST=<smtp-host>
EMAIL_PORT=<smtp-port>
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>
EMAIL_USE_TLS=True
```

> ⚠️ In local development with Docker Compose, `db` and `redis` refer to the service names in `docker-compose.yml`.

### 3. Run with Docker

```bash
docker compose build
docker compose up -d
```

This starts:
- **Web (Django)**
- **Postgres**
- **Redis**

### 4. Run migrations inside the container

```bash
docker compose exec web python manage.py migrate
```

### 5. Create superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 6. Seed sample data (optional)

```bash
docker compose exec web python manage.py seed
```

---

## Running Without Docker

1. Create virtual environment & install requirements:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Configure `.env` file with SQLite or Postgres.

3. Run migrations & server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

## API Documentation

Swagger documentation available at:

```
http://127.0.0.1:8000/documentation/
```

---

## Order Flow

1. User places an order with multiple books.  
2. Stock is verified before order creation.  
3. Total amount is calculated automatically.  
4. Email notification is sent to user and admin.  
5. Admin can update order status:  
   - `pending`  
   - `shipped`  
   - `delivered`  
   - `canceled`  

---

## Throttling

Default DRF throttling:  
- Anonymous users: **20 requests/day**  
- Authenticated users: **50 requests/day**

Can be customized per role.

---

## Deployment

### Render / Cloud Deployment
- Build & run the **Django app container**.  
- Use managed **Postgres** and **Redis** services (instead of Docker Compose).  
- Set environment variables (`DATABASE_URL`, `REDIS_URL`, `SECRET_KEY`, etc.) in the dashboard.  
- Run migrations once:  
  ```bash
  python manage.py migrate
  ```

---

## Contributing

1. Fork the repository  
2. Create a branch: `git checkout -b feature-name`  
3. Commit changes: `git commit -m "Add feature"`  
4. Push: `git push origin feature-name`  
5. Create a Pull Request  

---
