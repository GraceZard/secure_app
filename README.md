# ButterflyShop

A secure Django-based e-commerce application with enterprise-grade security features, inventory management, shopping cart functionality, and comprehensive audit logging.

## Table of Contents
- [Project Description](#project-description)
- [Security Features](#security-features-summary)
- [Installation Steps](#installation-steps)
- [How to Run the App](#how-to-run-the-app)
- [Dependencies](#dependencies)
- [Screenshots](#screenshots)

---

## Project Description

**Secure Shopping Application** is a full-featured e-commerce web application built with Django that demonstrates best practices for secure web development. The application includes:

### Core Features
- **User Authentication & Authorization**: Custom user model with secure password hashing (Argon2) and role-based access control
- **Product Inventory Management**: Add, edit, delete, and manage product listings with images and pricing
- **Shopping Cart**: Dynamic shopping cart with order history tracking
- **User Profiles**: Personalized user accounts with audit-able activities
- **Audit Logging**: Complete activity tracking with timestamps and action records for compliance and monitoring
- **Admin Dashboard**: Django admin interface for system management

### Intended Use
This application serves as both a functional e-commerce platform and a demonstration of security-hardened Django development practices suitable for production environments.

---

## Security Features Summary

The application implements comprehensive security controls across multiple layers:

### Authentication & Password Security
- **Argon2 Password Hashing**: Uses the Argon2 hasher as the primary algorithm (memory-hard, resistant to GPU/ASIC attacks)
- **Strong Password Validators**: Enforces password complexity rules including minimum length and dictionary checks
- **Custom Authentication Backend**: Supports login with username or email for enhanced user experience

### Session & Cookie Security
- **HttpOnly Cookies**: Session and CSRF cookies cannot be accessed via JavaScript (prevents XSS attacks)
- **Secure Session Lifecycle**: Sessions terminate when browser closes, limiting exposure window
- **Session Timeout**: Automatic session expiration configured for user safety

### CSRF Protection
- **CSRF Middleware**: Django's built-in CSRF token validation on all state-changing requests
- **HttpOnly CSRF Cookies**: Tokens stored securely and cannot be accessed by malicious scripts

### HTTP Security Headers
- **X-Frame-Options: DENY**: Prevents clickjacking attacks by blocking frame embedding
- **X-Content-Type-Options**: Prevents MIME-type sniffing attacks
- **XSS Filter**: Enables browser-based XSS attack mitigation

### HTTPS & Transport Security (Production-Ready)
- **SSL/TLS Configuration**: HSTS headers configured for production deployment
- **Secure SSL Redirect**: Ready to enforce HTTPS-only communication
- **Preload Support**: HSTS preload configured for inclusion in browser preload lists

### Audit & Compliance
- **Activity Logging**: Auditlog middleware tracks all database model changes with:
  - Timestamp of each action
  - User performing the action
  - Action type (create, update, delete)
  - Changed field values
- **Admin Audit View**: Dedicated audit log interface for compliance monitoring
- **Role-Based Access Control**: Admin-only access to sensitive audit information

### Database Security
- **SQLite with Secure Configuration**: Development database with path-based security
- **Field-Level Validation**: Form and model-level data validation
- **Prepared Statements**: Django ORM prevents SQL injection

---

## Installation Steps

### Prerequisites
- Python 3.8+ (tested with Python 3.12)
- pip (Python package manager)
- Git (for cloning the repository)
- Virtual environment (recommended: venv, pipenv, or conda)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/secure_app.git
cd secure_app
```

### Step 2: Create a Virtual Environment
```bash
# Using venv (Python 3.3+)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Django Settings
Update [secure_app/settings.py](secure_app/settings.py) with your environment-specific settings:
```python
# CRITICAL: In production, set these:
DEBUG = False                           # Disable debug mode
SECRET_KEY = 'your-secure-secret-key'  # Use a strong, unique key
ALLOWED_HOSTS = ['yourdomain.com']     # Add your domain
SESSION_COOKIE_SECURE = True           # Enable for HTTPS
CSRF_COOKIE_SECURE = True              # Enable for HTTPS
SECURE_SSL_REDIRECT = True             # Force HTTPS
```

### Step 5: Initialize Database
```bash
# Create database tables and run migrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser
# Follow prompts to set username, email, and password
```

### Step 6: Create Media Directories (if not present)
```bash
mkdir -p media/product_images
```

### Step 7: (Optional) Load Test Data
```bash
python manage.py loaddata initial_data.json  # If available
```

---

## How to Run the App

### Start the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000/`

### Access Different Components

| Component | URL | Purpose |
|-----------|-----|---------|
| **Home** | `http://localhost:8000/` | Redirects to login |
| **Registration** | `http://localhost:8000/register/` | Create new account |
| **Login** | `http://localhost:8000/login/` | User authentication |
| **Profile** | `http://localhost:8000/profile/` | User profile management |
| **Inventory** | `http://localhost:8000/inventory/` | Product listing and management |
| **Cart** | `http://localhost:8000/cart/` | Shopping cart and checkout |
| **Audit Log** | `http://localhost:8000/audit-log/` | View activity history (admin only) |
| **Admin** | `http://localhost:8000/admin/` | Django admin interface |

### First-Time Usage Workflow

1. **Register**: Go to `/register/` and create a new account
2. **Login**: Use your credentials at `/login/`
3. **Browse Products**: Navigate to `/inventory/` to view available products
4. **Add to Cart**: Select products and add them to your shopping cart
5. **Checkout**: Complete your order through the checkout process
6. **View History**: Check `/profile/` to see your order history
7. **Admin Access**: Superusers can view `/audit-log/` to see all system activities

### Production Deployment
```bash
# Collect static files
python manage.py collectstatic --noinput

# Use a production server (e.g., Gunicorn)
gunicorn secure_app.wsgi:application --bind 0.0.0.0:8000 --workers 4

# Use a reverse proxy (nginx/Apache) in front
# Enable SSL/TLS certificates (Let's Encrypt recommended)
# Update ALLOWED_HOSTS, DEBUG=False, and security settings in settings.py
```

---

## Dependencies

### Core Framework
- **Django 6.0.6**: Web framework
- **asgiref 3.11.1**: ASGI library for async support

### Security & Authentication
- **argon2-cffi 25.1.0**: Argon2 password hashing algorithm
- **argon2-cffi-bindings 25.1.0**: C bindings for high-performance hashing
- **bcrypt 5.0.0**: Alternative password hashing library

### Database & ORM
- **sqlparse 0.5.5**: SQL parser utility for Django ORM
- **pycparser 3.0**: C parser for cffi

### Audit & Compliance
- **django-auditlog 3.4.1**: Model audit logging for tracking changes

### Utilities
- **python-dateutil 2.9.0.post0**: Date/time utilities
- **six 1.17.0**: Python 2/3 compatibility utilities
- **cffi 2.0.0**: C Foreign Function Interface
- **tzdata 2026.2**: Timezone database

### Installation Command
```bash
pip install -r requirements.txt
```

---

## Screenshots

### 1. Login Page
User authentication interface with secure password entry.

### 2. User Registration
New user account creation with password validation.

### 3. Product Inventory
Main product listing page showing available items with images and prices.

### 4. Product Management (Admin)
Add/Edit/Delete products with image upload capabilities.

### 5. Shopping Cart
Dynamic cart showing selected items with quantity adjustments and total pricing.

### 6. Checkout Process
Secure order review and completion interface.

### 7. Order History
User's past orders with status and details.

### 8. User Profile
Profile management page displaying account information.

### 9. Audit Log (Admin Only)
Complete activity log showing who did what and when - essential for compliance auditing.

### 10. Django Admin Dashboard
System administration interface for managing users, products, and system configuration.

---

## Security Best Practices Implemented

✅ **Password Security**: Argon2 hashing algorithm (GPU/ASIC resistant)  
✅ **CSRF Protection**: Token validation on state-changing requests  
✅ **XSS Prevention**: Context-aware template escaping + security headers  
✅ **Clickjacking Prevention**: X-Frame-Options set to DENY  
✅ **Session Security**: HttpOnly, secure, and time-limited sessions  
✅ **Audit Trail**: Complete activity logging for compliance  
✅ **Role-Based Access**: Admin-only audit log access  
✅ **Production-Ready Configuration**: HSTS, SSL/TLS prepared  

---

## Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001  # Use different port
```

### Database Errors
```bash
python manage.py migrate --run-syncdb  # Force sync
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
```

### Permission Denied on Media Upload
```bash
chmod -R 755 media/  # macOS/Linux
```

---

## License

This project is provided for educational and demonstration purposes.

---

## Support & Contributing

For issues, questions, or contributions, please refer to the project repository or contact the development team.

**Last Updated**: 2026-06-18
