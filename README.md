# FastAPI Auth Service

This is a FastAPI-based authentication service with Role-Based Access Control (RBAC).

## Prerequisites

Before you begin, ensure you have met the following requirements:

*   **Docker and Docker Compose:** Used for running the PostgreSQL database and the FastAPI application.
*   **Python 3.10+:** (Optional, if running FastAPI app locally) The language runtime for the FastAPI application.
*   **pip:** (Optional, if running FastAPI app locally) Python package installer.
*   **venv:** (Optional, if running FastAPI app locally) Python virtual environment manager.

## Setup & Running with Docker Compose (Recommended)

This project is set up to run entirely with Docker Compose, which simplifies dependency management (PostgreSQL, FastAPI app).

### 1. Clone the repository

```bash
git clone https://github.com/walidozich/Auth-Service.git
cd fastapi-auth/auth-service
```

### 2. Create `.env` File

Create a `.env` file in the `auth-service` directory. This file will hold your environment variables.

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/authdb
SECRET_KEY=your_super_secret_key_here # Replace with a strong, random key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Note:** For `SECRET_KEY`, generate a strong, random string (e.g., using `openssl rand -hex 32`).

### 3. Build and Start Services

Build the Docker images and start the PostgreSQL database and FastAPI application services in detached mode:

```bash
docker compose up -d --build
```

Wait a few seconds for the database to fully initialize and become healthy. You can check the service status with:

```bash
docker compose ps
docker compose logs db
```

### 4. Run Database Migrations

Once the services are up, run the Alembic database migrations from within the `api` service container:

```bash
docker compose exec api alembic upgrade head
```

### 5. Access the Application

The FastAPI application will be accessible at `http://localhost:8000`. You can view the API documentation (Swagger UI) at `http://localhost:8000/docs`.

## Testing Role-Based Access Control (RBAC)

You can test the implemented RBAC by creating users with different roles and attempting to access a protected admin endpoint.

### 1. Create Users

**Create a regular user (default role is `USER`):**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "email": "user@example.com",
  "username": "regularuser",
  "password": "password123"
}'
```

**Create an admin user:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@example.com",
  "username": "adminuser",
  "password": "adminpassword",
  "role": "admin"
}'
```

### 2. Login to Get Tokens

**Login as regular user:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=regularuser&password=password123"
```
Copy the `access_token` from the response.

**Login as admin user:**

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=adminuser&password=adminpassword"
```
Copy the `access_token` from the response.

### 3. Test Admin Endpoint Access

**Attempt to access admin endpoint as regular user:**

```bash
curl -X GET "http://localhost:8000/api/v1/auth/admin/me" \
-H "Authorization: Bearer <REGULAR_USER_ACCESS_TOKEN>"
```
Expected result: `403 Forbidden`

**Access admin endpoint as admin user:**

```bash
curl -X GET "http://localhost:8000/api/v1/auth/admin/me" \
-H "Authorization: Bearer <ADMIN_USER_ACCESS_TOKEN>"
```
Expected result: `200 OK` with admin user details.

## Running Locally (Advanced)

If you prefer to run the FastAPI application directly on your host machine while still using the Dockerized PostgreSQL database:

### 1. Start Database Only

Ensure your `docker-compose.yml` maps the database to a non-conflicting port (e.g., `5433:5432` for `db` service).

```bash
docker compose up -d db
```

### 2. Virtual Environment and Dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. `.env` Configuration

Your `.env` file should contain:

```
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5433/authdb
SECRET_KEY=your_super_secret_key_here
ACCESS_TOKEN_EXPIRE_MINUTES=30
```
(Note the `localhost:5433` for connecting to the Dockerized DB from the host)

### 4. Run Migrations (if needed)

If you haven't run migrations via Docker Compose, or if you need to run them locally for some reason:

```bash
source venv/bin/activate
alembic upgrade head
```
**Important:** Ensure `alembic.ini` also points to `localhost:5433` for this local migration scenario.

### 5. Start FastAPI Application

```bash
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
