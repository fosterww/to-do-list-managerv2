# Task Manager API

A RESTful API for managing tasks, built with **FastAPI**, **SQLAlchemy**, and designed for easy deployment on platforms like **Render**.

---

## Features

- Create, read, update, and delete tasks
- Task status management (`todo`, `in_progress`, `completed`)
- FastAPI interactive documentation at `/docs`
- API key authentication (via `X-API-Key` header)
- Easy local or cloud deployment (SQLite/PostgreSQL)

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/fosterww/to-do-list-managerv2.git
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/Mac
venv\Scripts\activate        # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

To use PostgreSQL instead:

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
```

---

## Run the Application

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

📄 API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

All endpoints require an `X-API-Key` header.

### Create a Task

```http
POST /tasks/
```

```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{"title":"Test Task","description":"Test","status":"todo"}'
```

---

### 🔹 List Tasks

```http
GET /tasks/
```

```bash
curl "http://localhost:8000/tasks/" \
  -H "X-API-Key: your-secret-api-key"
```

---

### Get a Task by ID

```http
GET /tasks/{id}
```

```bash
curl "http://localhost:8000/tasks/1" \
  -H "X-API-Key: your-secret-api-key"
```

---

### Update a Task

```http
PUT /tasks/{id}
```

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{"title":"Updated Task"}'
```

---

### Delete a Task

```http
DELETE /tasks/{id}
```

```bash
curl -X DELETE "http://localhost:8000/tasks/1" \
  -H "X-API-Key: your-secret-api-key"
```

---

## Deployment (Render.com)

1. Create a [Render](https://render.com) account and connect your GitHub repository.
2. Set up a **Web Service** with:
   - **Build Command**:  
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command**:  
     ```bash
     gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
     ```
3. Add a PostgreSQL add-on and configure the `DATABASE_URL` environment variable.

After deployment, you’ll be able to access your live API from the provided Render URL.

---

##  Contact

- **GitHub**: [fosterww](https://github.com/fosterww)