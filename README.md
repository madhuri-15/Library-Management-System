
# Library Management System API

This API provides functionalities for managing a library system, allowing librarians (admins) to manage users and book borrow requests, while library users can request books and view their borrowing history.

### Features
#### Librarian APIs
- Create new library users with email and password.
- View all book borrowing requests.
- Approve or deny borrow requests.
- View a user's book borrowing history.

#### Library User APIs
- View the list of books in the library.
- Submit a request to borrow a book for specific dates.
- View personal book borrowing history.
- Download borrowing history as a CSV file.

### Technologies Used
- Programming Language: Python
- Framework: Flask
- Database: MySQL (using SQLAlchemy ORM)
- Authentication: JSON Web Tokens (JWT)
- API Testing: Postman

### Database Schema
***Users***
```
id        
email
password
is_admin
```
***Books***
```
id
title
author
published_year
```
***Requests***
```
id
user_id
book_id
start_date
end_date
status (Pending, Denied, Approved)
```

### Setup and Installation
1. Clone the Repository

```bash
git clone https://github.com/madhuri-15/Library-Management-System.git
cd Library-Management-System
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Configure the Database

Update the configuration with your MySQL database credentials.
```bash
SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost:port/library_db'
SECRET_KEY = 'your_secret_key'
```
4. Run the Application
```bash
python run.py
```

### API Endpoints
#### Create Admin Account
- SignUp: /signup (POST)

#### Authentication
- Login: /login (GET)
- Logout: /logout (POST)

#### Librarian APIs
- Create User: /add-user (POST)
- Add Book: /add-book (POST)
- View All Borrow Requests: /requests (GET)
- Approve/Deny Request: /requests/<request_id> (PUT)
- View User History: /users/<user_id>/history (GET)

#### Library User APIs
- Get List of Books: /books (GET)
- Submit Borrow Request: /request-book (POST)
- View Borrow History: /user/history (GET)
- Download Borrow History (CSV): /user/download-history (GET)

### Authentication
This API uses JWT-based authentication.

All admin and user requests must include the JWT token in the Authentication header:

```javascript
Authentication: <JWT Token>
```
You can use this test [data](https://github.com/madhuri-15/Library-Management-System/blob/main/data.txt)

