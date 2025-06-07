# Le Grand - Backend

Welcome to the backend of **Le Grand**, a small artisanal bakery specialized in breads, cookies, and sweets.

This project provides a backend service built with **FastAPI**, using **PostgreSQL** to persist most business data and **MongoDB** to store customer orders — this design ensures that order data remains immutable, even if product prices change in the future.

## 🧰 Features

- JWT Authentication & Authorization
  - Two roles: `ADMIN` and `CUSTOMER`
  - All routes are protected except `image` and `reset`
- PostgreSQL for most relational data
- MongoDB for order-related data
- Route to reset and populate databases with demo data (not available in production)
- Image route meant to be handled by an external image service in production (e.g., Cloudinary)

---

## 🚀 Getting Started

### 1. Prerequisites

Make sure you have the following installed:

- [Docker](https://docs.docker.com/)
- [Python](https://www.python.org/)

---

### 2. Clone the Repository

```bash
git clone https://github.com/markinh00/le-grand-backend.git
cd le-grand-backend
```
### 3. Environment Configuration
Create a .env file at the root of the project with the variables bellow:
```bash
API_KEY=YOUR_API_KEY

SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

POSTGRES_URI=postgresql://postgres:postgres@postgresql:5432/le-grand

IMAGE_DIR=./images
DEFAULT_IMAGE_URL=http://localhost:8000/image/default-placeholder.png

MONGODB_HOST=mongo:27017
MONGODB_USER=root
MONGODB_PASSWORD=example
MONGODB_DATABASE=le-grand
MONGODB_COLLECTION=orders
```
### 4. Running the Project
Run the backend, PostgreSQL, MongoDB, and Mongo Express:
```bash
docker-compose up --build
```
This will:
 - Start the FastAPI backend on http://localhost:8000
 - Start PostgreSQL on port 5432
 - Start MongoDB on port 27017
 - Expose Mongo Express (MongoDB GUI) at http://localhost:8081

### 5. API Routes
After starting the project, access the API documentation at:
 - Swagger UI: http://localhost:8000/docs
 - Redoc: http://localhost:8000/redoc

### ⚠️ Important Notes
image and reset routes are public for development/demo purposes only:
 - image: would be handled by services like Cloudinary in production
 - reset: deletes all data in both databases and repopulates them with demo data

These routes should be removed before deploying to production

### 📁 Volumes
PostgreSQL data is persisted in the postgres_data volume.
Uploaded images are stored in the ./images directory (mounted as a volume)

### 🛡️ Authenticated Routes
Most routes are protected and require a JWT token:
 - Get a token via auth/login or auth/register
 - Use the token as a Bearer token in the Authorization header
#### login example:
![image](https://github.com/user-attachments/assets/5debfdad-e7d8-40f7-b9dd-fec5ab9976cb)
#### register example:
![image](https://github.com/user-attachments/assets/d833022f-b75f-4231-aad0-4c389c95f8fa)

