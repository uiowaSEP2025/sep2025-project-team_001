[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/4tPelvOm)

# Project Setup Instructions

---

## 1. Install Docker (and Docker Compose)

1. **Windows / Mac**:  
   - Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).  
   - Docker Desktop **includes** Docker Compose, so you’re all set.
2. **Linux**:  
   - Install [Docker Engine](https://docs.docker.com/engine/install/) for your distribution (Ubuntu, Debian, etc.).  
   - Install [Docker Compose](https://docs.docker.com/compose/install/) if it’s not included in your package manager.

**Verify** your installation:
```bash
docker --version
docker compose version
```

---

## 2. Create `.env` file

Create a `.env` file in the root of the project directory with the following content:
```
DB_NAME=TestDatabase
DB_USER=TestUser
DB_PASS=password
DJANGO_SECRET_KEY='django-insecure-e#^3(&8y3by5n-2$a%756r!s(#x1^_v!%jbprj-6b2-4hl5-fn'
REACT_APP_API_URL=http://localhost:8000/auth/
```

---

## 3. Build and Run the Project

1. Build the project:  
```bash
docker compose -f ./docker-compose-all-local.yml up --build
```

2. Run PostgreSQL migrations:
```bash
docker compose -f ./docker-compose-all-local.yml exec backend python manage.py makemigrations
docker compose -f ./docker-compose-all-local.yml exec backend python manage.py migrate
```

---

## 4. Access the Project

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend**: [http://localhost:8000](http://localhost:8000)
- **DB Logs**: `docker compose logs db`
- **Backend Logs**: `docker compose logs backend`
- **Frontend Logs**: `docker compose logs frontend`

---

## 5. Stop the Project

1. Stop the project (Keep local DB volumes):  
```bash
docker compose down
```

**OR**

2. Remove all volumes as well:  
```bash
docker compose down --volumes
```

