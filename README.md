# Bell Assessment - Backend API

A Flask-based REST API for user management with file upload capabilities and SQL Server database integration.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [File Upload](#file-upload)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Features

- **User Management**: Create, read, update, and delete user profiles
- **File Upload**: Support for image uploads (JPG, JPEG, PNG)
- **REST API**: Comprehensive RESTful endpoints with JSON responses
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
- **SQL Server Integration**: Secure database connections with ODBC Driver
- **Error Handling**: Proper HTTP status codes and error messages
- **Data Validation**: Required field validation and file type checking

## Project Structure

```
BackendAPI/
├── app/                          # Application package
│   ├── __init__.py              # App factory and initialization
│   ├── config.py                # Configuration settings
│   ├── models.py                # Database models (User, etc.)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── users.py             # User routes and endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py      # Business logic for user operations
│   └── utils/
│       └── file_handler.py      # File upload and handling utilities
├── tests/
│   └── test_users.py            # Unit tests for user endpoints
├── uploads/
│   └── photos/                  # Directory for user photo uploads
├── app.py                        # Legacy Flask app (for reference)
├── run.py                        # Application entry point
├── test.py                       # Test fixtures and setup
├── utils.py                      # Utility functions
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

<img width="1536" height="1024" alt="architecture" src="https://github.com/user-attachments/assets/51552195-b372-412d-8b1f-d590576e9a82" />


## Prerequisites

- **Python**: 3.7 or higher
- **SQL Server**: MSSQL Server with ODBC Driver 17 installed
- **ODBC Driver**: Microsoft ODBC Driver 17 for SQL Server
- **pip**: Python package manager

## Installation

### 1. Clone or Download Project

```bash
cd d:\Bell_Assessment\BackendAPI
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install flask flask-sqlalchemy flask-cors pyodbc
```

Or install from requirements.txt (if populated):

```bash
pip install -r requirements.txt
```

### 4. Install ODBC Driver (Windows)

If using SQL Server, download and install [Microsoft ODBC Driver 17 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

## Configuration

### Environment Variables

Create a `.env` file in the root directory (optional):

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=mssql+pyodbc:///?odbc_connect=DRIVER={ODBC Driver 17 for SQL Server};SERVER=your_server;DATABASE=your_db;Trusted_Connection=yes;
UPLOAD_FOLDER=uploads/photos
```

### Application Settings

Edit `app/config.py` for default configuration:

```python
class Config:
    SECRET_KEY = "dev-secret-key"
    SQLALCHEMY_DATABASE_URI = "mssql+pyodbc:///?odbc_connect=..."
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "uploads/photos"
```

#### Current Database (app/config.py)
- **Type**: MySQL
- **Host**: localhost
- **Port**: 3306
- **Database**: flask_crud
- **Default Credentials**: myadmin / 123456

**Note**: Update these credentials for production environments using environment variables.

## Running the Application

### Start the Development Server

```bash
python run.py
```

The API will be available at: `http://localhost:5000`

### Debug Mode

The application runs with `debug=True` by default. This enables:
- Auto-reloading on code changes
- Enhanced error messages
- Interactive debugger

## API Endpoints

### Base URL
```
http://localhost:5000/api/users
```

### Endpoints

#### 1. Get All Users
```http
GET /api/users/
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "image": "profile.jpg"
  }
]
```

#### 2. Get User by ID
```http
GET /api/users/<user_id>
```

**Parameters**:
- `user_id` (integer): The user's unique identifier

**Response (200 OK)**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "image": "profile.jpg"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

#### 3. Create User
```http
POST /api/users/
Content-Type: multipart/form-data
```

**Required Fields**:
- `first_name` (string): User's first name
- `last_name` (string): User's last name
- `email` (string): User's email address
- `password` (string): User's password
- `image` (file, optional): User's profile photo (JPG, JPEG, PNG)

**Example Request** (using curl):
```bash
curl -X POST http://localhost:5000/api/users/ \
  -F "first_name=John" \
  -F "last_name=Doe" \
  -F "email=john@example.com" \
  -F "password=securepassword123" \
  -F "image=@profile.jpg"
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "image": "profile.jpg"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Missing fields: first_name, email"
}
```

#### 4. Update User
```http
PUT /api/users/<user_id>
Content-Type: multipart/form-data
```

**Parameters**:
- `user_id` (integer): The user's unique identifier

**Optional Fields**:
- `first_name` (string)
- `last_name` (string)
- `email` (string)
- `password` (string)
- `image` (file)

**Example Request**:
```bash
curl -X PUT http://localhost:5000/api/users/1 \
  -F "first_name=Jane" \
  -F "image=@new_profile.jpg"
```

**Response (200 OK)**:
```json
{
  "message": "User updated successfully"
}
```

#### 5. Delete User
```http
DELETE /api/users/<user_id>
```

**Parameters**:
- `user_id` (integer): The user's unique identifier

**Response (200 OK)**:
```json
{
  "message": "User deleted successfully"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

## Database Models

### User Model

Located in `app/models.py`

**Schema**:
```python
class User(db.Model):
    __tablename__ = 'users'
    
    id              : Integer (Primary Key)
    first_name      : String(50)
    last_name       : String(50)
    email           : String(100)
    password        : String(100)
    image           : String(200)  # Filename of uploaded image
```

**Methods**:
- `to_dict()`: Converts user instance to dictionary (excludes password)

## File Upload

### Upload Configuration

- **Location**: `uploads/photos/`
- **Allowed Types**: JPG, JPEG, PNG
- **Max File Size**: Configurable (default: unlimited)

### Upload Process

1. User submits POST request with image file
2. Filename is secured using `werkzeug.security.secure_filename()`
3. File is saved to `uploads/photos/` directory
4. Only the filename is stored in the database

### Security Considerations

- Only image files are allowed (validated by extension)
- Filenames are sanitized to prevent directory traversal attacks
- Consider implementing file size limits for production

## Testing

### Run Tests

```bash
python test.py
```

Or using pytest (if installed):

```bash
pytest tests/test_users.py -v
```

### Test Coverage

- `tests/test_users.py`: User endpoint tests
  - GET all users
  - GET user by ID
  - POST new user
  - PUT update user
  - DELETE user

## Troubleshooting

### Issue: "Import flask could not be resolved"

**Solution**:
1. Activate virtual environment: `venv\Scripts\activate`
2. Install dependencies: `pip install flask flask-sqlalchemy flask-cors pyodbc`
3. Restart VS Code
4. Select correct Python interpreter in VS Code

### Issue: Database Connection Error

**Solution**:
1. Verify SQL Server is running
2. Check connection string in `app/config.py`
3. Ensure ODBC Driver 17 is installed
4. Verify database credentials and permissions

### Issue: Permission Denied on File Upload

**Solution**:
1. Ensure `uploads/photos/` directory exists and is writable
2. Create directory if missing: `mkdir -p uploads/photos`
3. Check folder permissions

### Issue: CORS Error

**Solution**:
- CORS is enabled by default in the application
- If issues persist, verify `flask-cors` is installed
- Check frontend request headers

## Development Notes

- **Debug Mode**: Currently enabled for development. Disable in production.
- **Database**: Switch from MySQL to SQL Server as needed (update connection string in config)
- **Password Security**: Implement password hashing (bcrypt, argon2) before production
- **Validation**: Add additional input validation and sanitization
- **Authentication**: Implement JWT tokens or session-based authentication for production

## License

This project is part of the Bell Assessment.

---

**Last Updated**: February 15, 2026
