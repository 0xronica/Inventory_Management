Project Overview

The Inventory Management API is a backend application built using Django and Django REST Framework. It allows businesses or individuals to efficiently manage inventory items, track stock levels, and manage user access. The API provides CRUD (Create, Read, Update, Delete) operations for inventory items and users, as well as role-based access control to ensure data security.

This project solves the problem of manual inventory tracking, providing real-time updates, change logs, and structured permissions for owners and workers managing stock.

Features
Inventory Management

Create, Read, Update, Delete (CRUD) operations for inventory items.

Inventory item attributes include:

Name

Description

Quantity

Price

Category

Date Added

Last Updated

Validation to ensure required fields are provided.

User Management

CRUD operations for users.

Users have unique username, email, and password.

Roles supported:

Owner – full access

Worker – limited access

Only authenticated users can manage inventory items.

Users can only modify inventory items they own.

Inventory Change Tracking

Logs every change in inventory quantity.

Records include:

Item updated

User who made the change

Old and new quantity

Timestamp

Authentication

JWT (JSON Web Token) authentication for secure API access.

Only active and authorized users can access protected endpoints.

Filtering, Searching, and Pagination

View inventory by category or price range.

Filter items by low stock (below a threshold).

Paginate large datasets for efficient performance.

Technical Stack

Backend Framework: Django, Django REST Framework

Database: SQLite (development), PostgreSQL/MySQL recommended for production

Authentication: Django’s built-in system with JWT (SimpleJWT)

Deployment: PythonAnywhere or Heroku

API Endpoints
Users
Method	Endpoint	Description
POST	/api/auth/login/	Get JWT token using username & password
POST	/api/users/	Create a new user
GET	/api/users/	List all users
GET	/api/users/{id}/	Retrieve user details
PUT/PATCH	/api/users/{id}/	Update user information
DELETE	/api/users/{id}/	Delete a user
Inventory Items
Method	Endpoint	Description
GET	/api/items/	List all inventory items
POST	/api/items/	Create a new inventory item
GET	/api/items/{id}/	Retrieve inventory item details
PUT/PATCH	/api/items/{id}/	Update an inventory item
DELETE	/api/items/{id}/	Delete an inventory item
Inventory Change Log
Method	Endpoint	Description
GET	/api/item-changes/	View inventory change history
Example Code Snippets
Create a User
from users.models import User

User.objects.create_user(
    username="owner1",
    password="testpass123",
    role="owner"
)

Create an Inventory Item
from inventory.models import InventoryItem
from users.models import User

owner = User.objects.get(username="owner1")

InventoryItem.objects.create(
    owner=owner,
    name="Laptop",
    description="Dell Latitude",
    quantity=10,
    price=500000,
    category="Electronics"
)

Authenticate User (JWT)
POST /api/auth/login/
{
    "username": "owner1",
    "password": "testpass123"
}


Response:

{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}

Deployment Instructions

Clone the repository:

git clone <repository_url>


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Deploy on PythonAnywhere or Heroku and configure environment variables for production.

Testing

Use Postman to test API endpoints.

Test different roles:

Owner → full access

Worker → limited access

Check low-stock filters and inventory change logs.

Project Structure
inventory_api/
├── users/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── inventory/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── inventory_api/
│   ├── settings.py
│   ├── urls.py
├── manage.py
