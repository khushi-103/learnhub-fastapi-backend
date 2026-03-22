# LearnHub FastAPI Backend

A simple backend API for an online learning platform built using **FastAPI**.
This project was created as a practice exercise to understand how REST APIs work in Python, including course management, enrollments, search and filtering, pagination, and wishlist functionality.

The API simulates the backend of a basic course platform.

---

## Features

### Course Management

- View all available courses
- Get course details using course ID
- Add new courses
- Update course price or available seats
- Delete courses (only if no students are enrolled)

### Course Discovery

- Search courses using keywords
- Filter courses by category, level, price, and seat availability
- Sort courses by price, title, or seats left
- Pagination support for large course lists
- Combine filters and sorting for advanced browsing

### Enrollment System

- Enroll students into courses
- Early bird discount when more than 5 seats are available

**Coupon Support**

- `STUDENT20` → 20% discount
- `FLAT500` → ₹500 discount

**Additional Option**

- Gift enrollment for another student

### Wishlist System

- Add courses to a wishlist
- Prevent duplicate wishlist entries
- View wishlist courses
- Remove courses from wishlist
- Enroll in all wishlist courses at once

### Enrollment Management

- View all enrollments
- Search enrollments by student name
- Sort enrollments by final fee
- Paginate enrollment records

---

## Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn

---

## Project Structure

## Project Structure

```
learnhub-fastapi-backend
│
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── output
    ├── output1.png
    ├── output2.png
    ├── output3.png
    └── ... (API screenshots and test results)
```

---

## Setup and Installation

### 1. Clone the repository

```
git clone https://github.com/khushi-103/learnhub-fastapi-backend.git
```

### 2. Navigate to the project folder

```
cd learnhub-fastapi-backend
```

### 3. Create a virtual environment

```
python -m venv venv
```

### 4. Activate the virtual environment

**Windows**

```
venv\Scripts\activate
```

**Mac/Linux**

```
source venv/bin/activate
```

### 5. Install dependencies

```
pip install -r requirements.txt
```

---

## Running the Server

Start the FastAPI application with:

```
uvicorn main:app --reload
```

The server will start at:

```
http://127.0.0.1:8000
```

---

## API Documentation

FastAPI automatically generates interactive documentation.

**Swagger UI**

```
http://127.0.0.1:8000/docs
```

**ReDoc**

```
http://127.0.0.1:8000/redoc
```

You can test all API endpoints directly from the browser.

---

## Example API Endpoints

Get all courses

```
GET /courses
```

Search courses

```
GET /courses/search?keyword=python
```

Filter courses

```
GET /courses/filter?category=Web Dev
```

Enroll in a course

```
POST /enrollments
```

Add a course to wishlist

```
POST /wishlist/add?student_name=Rahul&course_id=2
```

---

## Future Improvements

Some possible improvements for the project:

- Add a database (PostgreSQL or SQLite)
- Implement user authentication
- Add instructor accounts
- Add course reviews and ratings
- Create a frontend for the platform

---

## Purpose of the Project

The goal of this project was to practice building backend APIs using FastAPI and understand concepts like:

- REST API design
- Request handling
- Data validation with Pydantic
- Query parameters for search, filtering, and pagination

---
