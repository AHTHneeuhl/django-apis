# 💰 Expense Tracker API (FastAPI)

A production-ready Expense Tracker backend built using **FastAPI**, featuring JWT authentication, category normalization, reporting endpoints, CSV export, and Docker support.

---

## 🚀 Features

### 🔐 Authentication

- User registration
- JWT-based login
- Protected routes
- User-specific data isolation

### 💳 Transactions

- Create income & expense transactions
- Update & delete transactions
- Filter by:
  - Type (income / expense)
  - Category
  - Date range

- Enum validation for transaction type

### 📂 Categories

- Separate normalized category table
- Foreign key relationship with transactions

### 📊 Reporting

- Monthly summary (income, expense, net savings)
- Yearly monthly expense chart data
- Aggregated financial reporting endpoints

### 📤 Export

- Export transactions to CSV
- Supports filtering before export

### 🐳 Deployment Ready

- Dockerized
- Environment variable configuration
- Production-compatible structure

---

## 🏗 Tech Stack

- FastAPI
- SQLAlchemy (ORM)
- SQLite (Dev) / PostgreSQL (Production)
- JWT (python-jose)
- Passlib (bcrypt hashing)
- Pandas (CSV export)
- uv (Python package manager)
- Docker

---

## 📁 Project Structure

```
expense_tracker/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   └── routes/
│       ├── auth.py
│       ├── transactions.py
│       ├── categories.py
│       └── reports.py
│
├── Dockerfile
├── .dockerignore
├── pyproject.toml
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions (Local Development)

### 1️⃣ Clone Repository

```bash
git clone <your-repo-url>
cd beginner/expense_tracker
```

### 2️⃣ Install Dependencies

Using `uv`:

```bash
uv sync
```

Activate virtual environment:

```bash
source .venv/bin/activate
```

### 3️⃣ Configure Environment Variables

Create `.env` file:

```
DATABASE_URL=sqlite:///./expense_tracker.db
SECRET_KEY=your-secret-key
```

### 4️⃣ Run Server

```bash
uv run uvicorn app.main:app --reload
```

Open API docs:

```
http://127.0.0.1:8000/docs
```

---

## 🔐 Authentication Flow

1. Register:

```
POST /auth/register
```

2. Login:

```
POST /auth/login
```

3. Use returned JWT token:

```
Authorization: Bearer <access_token>
```

All transaction and report routes require authentication.

---

## 📊 Reporting Endpoints

### Monthly Summary

```
GET /reports/monthly?month=2&year=2026
```

### Monthly Chart Data

```
GET /reports/monthly-chart?year=2026
```

### CSV Export

```
GET /reports/export-csv
```

Supports filtering:

```
/reports/export-csv?type=expense
```

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t expense-tracker .
```

### Run Container

```bash
docker run -p 8000:8000 expense-tracker
```

---

## 🌍 Production Deployment

Recommended:

- Render
- Railway

For production:

- Use PostgreSQL
- Set environment variables securely
- Never commit `.env`

---

## 🧠 Architecture Highlights

- Clean modular structure
- Proper database normalization
- Enum-based validation
- JWT authentication
- User-level data isolation
- Aggregation queries using SQL functions
- File streaming for CSV export

---
