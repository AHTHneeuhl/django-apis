# 📌 Task Manager API

A production-ready RESTful Task Management API built with **Django** and **Django REST Framework**.

This project is part of a monorepo architecture and is deployed publicly using Render.

---

## 🌍 Live URL

🔗 https://task-manager-vryh.onrender.com

---

## 🛠 Tech Stack

- Python 3.12
- Django
- Django REST Framework (DRF)
- Gunicorn (WSGI server)
- SQLite (structured for PostgreSQL upgrade)
- WhiteNoise (static file handling)
- Render (cloud deployment)

---

## ✨ Features

- User registration
- Token-based authentication
- CRUD operations for tasks
- User-specific task ownership
- Production-ready configuration
- Monorepo deployment setup
- Environment-based settings
- Static file handling

---

## 🔗 API Endpoints

### 🔐 Authentication

POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/

### 📋 Tasks

POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/token/refresh/

> All task endpoints require authentication.

---

## 🔐 Authentication Details

After successful login, you will receive an access token.

Include the token in your request headers:

Authorization: Bearer <your_access_token>

Requests without a valid token will be denied.

---

## 💻 Local Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AHTHneeuhl/django-apis.git
cd django-apis/beginner/task_manager

python -m venv venv
source venv/bin/activate

pip install -r ../../requirements.txt

python manage.py migrate

python manage.py createsuperuser

python manage.py createsuperuser
```
