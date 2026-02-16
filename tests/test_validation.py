"""
Data Validation Unit Tests

Simple, focused unit tests for user input validation without database manipulation.
Tests cover: email format, password requirements, file extensions, data types,
and SQL injection detection.

Author: Backend API Team
Version: 1.0.0
"""

import re


def test_valid_email_format():
    """Valid email formats should pass validation."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    valid_emails = ["user@example.com", "john.doe@company.co.uk", "test123@domain.org"]
    
    for email in valid_emails:
        assert re.match(email_pattern, email)


def test_invalid_email_format():
    """Invalid email formats should fail validation."""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    invalid_emails = ["invalid.email", "@example.com", "user@", "user@.com", ""]
    
    for email in invalid_emails:
        assert not re.match(email_pattern, email)


def test_password_validation():
    """Password must be at least 8 characters and not empty."""
    def is_valid_password(password):
        return password and len(password.strip()) >= 8
    
    assert is_valid_password("password123")
    assert is_valid_password("12345678")
    assert not is_valid_password("pass")
    assert not is_valid_password("")
    assert not is_valid_password("   ")


def test_name_validation():
    """First and last names must be 2-100 characters."""
    def is_valid_name(name):
        return 2 <= len(name) <= 100 and name and len(name.strip()) > 0
    
    assert is_valid_name("John")
    assert is_valid_name("Mary-Jane")
    assert not is_valid_name("J")
    assert not is_valid_name("")
    assert not is_valid_name("A" * 101)


def test_allowed_file_extensions():
    """Only JPG, JPEG, PNG file extensions are allowed."""
    def allowed_file(filename):
        allowed = {"jpg", "jpeg", "png"}
        return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed
    
    assert allowed_file("profile.jpg")
    assert allowed_file("photo.png")
    assert allowed_file("image.JPEG")
    assert not allowed_file("script.exe")
    assert not allowed_file("document.pdf")
    assert not allowed_file("imagefile")


def test_user_id_validation():
    """User ID must be a positive integer."""
    def is_valid_id(user_id):
        return isinstance(user_id, int) and user_id > 0
    
    assert is_valid_id(1)
    assert is_valid_id(100)
    assert not is_valid_id(0)
    assert not is_valid_id(-1)
    assert not is_valid_id("1")


def test_sql_injection_detection():
    """Detect common SQL injection patterns."""
    def has_sql_injection(text):
        patterns = [r"'\s*OR\s*'", r";\s*DROP", r"UNION\s+SELECT", r"--"]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)
    
    assert has_sql_injection("' OR '1'='1")
    assert has_sql_injection("'; DROP TABLE users;")
    assert has_sql_injection("UNION SELECT * FROM users")
    assert not has_sql_injection("normal user input")
    assert not has_sql_injection("john@example.com")


def test_required_fields_validation():
    """Required fields must be present and not empty."""
    def validate_required(data, required_fields):
        return all(field in data and data[field] for field in required_fields)
    
    required = ["first_name", "last_name", "email", "password"]
    
    assert validate_required({
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "password123"
    }, required)
    
    assert not validate_required({
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com"
    }, required)


def test_complete_user_validation():
    """Complete user data validation with multiple rules."""
    def validate_user(data):
        errors = []
        
        required = ["first_name", "last_name", "email", "password"]
        for field in required:
            if field not in data or not data[field]:
                errors.append(f"{field} required")
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if "email" in data and not re.match(email_pattern, data["email"]):
            errors.append("Invalid email format")
        
        if "password" in data and len(data["password"]) < 8:
            errors.append("Password too short")
        
        if "first_name" in data and (len(data["first_name"]) < 2 or len(data["first_name"]) > 100):
            errors.append("First name length invalid")
        
        return len(errors) == 0, errors
    
    # Valid case
    valid, errors = validate_user({
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "password": "securepass123"
    })
    assert valid and len(errors) == 0
    
    # Invalid case
    valid, errors = validate_user({
        "first_name": "J",
        "last_name": "Doe",
        "email": "invalid",
        "password": "pass"
    })
    assert not valid and len(errors) > 0


def test_email_normalization():
    """Email should be normalized to lowercase."""
    def normalize_email(email):
        return email.lower() if isinstance(email, str) else email
    
    assert normalize_email("User@Example.COM") == "user@example.com"
    assert normalize_email("JOHN@DOMAIN.ORG") == "john@domain.org"
