# 📚 Library Management System (LMS API)

A production-ready RESTful API built using Django and Django REST Framework for managing a library system.

---

## 🚀 Features

* 🔐 JWT Authentication (Register/Login/Logout)
* 👥 Role-based access (Student / Librarian)
* 📚 Book Management (CRUD)
* ✍️ Author & Genre Management
* 📦 Borrow Request System
* ⭐ Book Reviews
* 🔍 Search & Filtering
* ↕️ Ordering Support
* 🚦 API Throttling (Rate Limiting)
* 📧 Email Notifications (Approve/Reject)
* 📄 Swagger & Redoc API Documentation

---

## 🛠 Tech Stack

* Python
* Django
* Django REST Framework (DRF)
* Simple JWT
* SQLite / MySQL
* drf-yasg (Swagger)

---

## 📁 Project Structure

```
lms_project/
├── accounts/
├── library/
├── lms_project/
├── manage.py
├── .env
├── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone https://github.com/nileshpatil8620/lms-api.git
cd lms-project
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Run Migrations

```
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser

```
python manage.py createsuperuser
```

---

### 6️⃣ Run Server

```
python manage.py runserver
```

---

## 🔐 Authentication APIs

| Endpoint            | Method | Description                    |
| ------------------- | ------ | ------------------------------ |
| /api/register/      | POST   | Register user                  |
| /api/login/         | POST   | Login user (JWT)               |
| /api/logout/        | POST   | Logout user                    |
| /api/token/         | POST   | Get JWT access & refresh token |
| /api/token/refresh/ | POST   | Refresh JWT token              |

---

## 📚 Core APIs

### Books

| Endpoint         | Method | Description              |
| ---------------- | ------ | ------------------------ |
| /api/books/      | GET    | List all books           |
| /api/books/      | POST   | Create a new book        |
| /api/books/{id}/ | GET    | Retrieve a specific book |
| /api/books/{id}/ | PUT    | Update a specific book   |
| /api/books/{id}/ | DELETE | Delete a specific book   |


### Book Review

| Endpoint                      | Method | Description             |
| ----------------------------- | ------ | ----------------------- |
| /api/books/{book_id}/reviews/ | GET    | List reviews for a book |
| /api/books/{book_id}/reviews/ | POST   | Add a review for a book |


### Authors

| Endpoint           | Method | Description                 |
| ------------------ | ------ | --------------------------- |
| /api/authors/      | GET    | List all authors            |
| /api/authors/      | POST   | Create a new author         |


### Genres

| Endpoint           | Method | Description                 |
| ------------------ | ------ | --------------------------- |
| /api/authors/      | GET    | List all authors            |
| /api/authors/      | POST   | Create a new author         |

### Borrow Management

| Endpoint | Method | Description |
|---|---|---|
| /api/borrow/ | POST | Request to borrow a book (student only) |
| /api/borrow/ | GET | List all requests of current user |
| /api/borrow/{id}/approve/ | PATCH | Approve borrow (librarian only) |
| /api/borrow/{id}/reject/ | PATCH | Reject request (librarian only) |
| /api/borrow/{id}/return/ | PATCH | Mark book as returned |

---

## 🔍 Filtering & Search

```
/api/books/?search=python
/api/books/?ordering=title
/api/books/?genres=1
/api/books/?author=1

---

## 🚦 Throttling

* Borrow API limited to **3 requests per day per user**

---

## 📧 Email Notification

* Users receive email on:

  * Approval
  * Rejection

---

## 📄 API Documentation

* Swagger UI: `/swagger/`
* Redoc UI: `/redoc/`

---

## 🧑‍💻 Author

Developed by Nilesh Patil

---

## 📌 Future Improvements

* Docker support
* AWS deployment
* React frontend
* Celery for async email

---
