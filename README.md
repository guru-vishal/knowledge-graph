# Personal Knowledge Graph System

A full-stack application for creating notes, organizing them with tags, and connecting ideas through directed links and backlinks.

## Features

- Create and retrieve notes
- Search notes by title or content
- Filter notes by tag
- Normalize tags and suggest existing tags
- Automatically resolve existing `[[Note Title]]` references into links
- View outgoing links and backlinks
- Manually create note links
- Retrieve the note-link graph
- Interactive API documentation through Swagger UI
- Generated Python SDK using OpenAPI Generator
- Automated backend tests

## Technology Stack

**Backend:** Python, FastAPI, SQLAlchemy, Pydantic

**Database:** SQLite, Alembic

**Frontend:** React, Vite, Axios

**Testing:** pytest, FastAPI TestClient

**SDK:** OpenAPI Generator CLI

## Prerequisites

- Python 3.10 or newer
- Node.js and npm
- Git Bash
- Java/JDK compatible with your installed OpenAPI Generator version (for SDK generation)

Docker is not required.

## Installation

Clone or extract the project and open Git Bash in its root directory.

Run the development setup script:

```bash
cmd.exe /c setupdev.bat
```

The script creates the Python virtual environment if necessary, installs dependencies, applies database migrations, and installs frontend dependencies.

## Running the Application

Start both services using:

```bash
cmd.exe /c runapplication.bat
```

Open the frontend at:

http://127.0.0.1:5173

Swagger UI:

http://127.0.0.1:8000/docs

OpenAPI specification:

http://127.0.0.1:8000/openapi.json

## Running the Backend Manually

```bash
source env/Scripts/activate
python -m uvicorn main:app --reload
```

## Running the Frontend Manually

Open another Git Bash terminal:

```bash
cd frontend
npm run dev
```

## Database Migrations

Create a new migration after modifying the SQLAlchemy models:

```bash
source env/Scripts/activate
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

Apply existing migrations:

```bash
alembic upgrade head
```

## Sample Data

The `seed_data.sql` file contains sample notes, tags, and relationships.

After applying migrations, it can be loaded into a clean development database using SQLite. Avoid running the script repeatedly against an already populated database because its explicit IDs and unique titles can conflict.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/notes/` | Create a note |
| GET | `/notes/` | List, search, or filter notes |
| GET | `/notes/{note_id}` | Retrieve note details and links |
| PATCH | `/notes/{note_id}/link` | Create a directed link |
| GET | `/notes/tags/suggestions` | List existing tags |
| GET | `/graph/` | Retrieve graph nodes and edges |
| GET | `/health` | Check API health |

### Search and filtering examples

```text
GET /notes/?keyword=Python
GET /notes/?tag=programming
GET /notes/?tag=programming&keyword=Python
```

### Link behavior

A note containing `[[Data Structures]]` automatically links to an existing note with that title when the source note is created. Backlinks are returned when retrieving the target note.

Links are directed. Duplicate links and self-links are rejected by the API.

## Running Tests

From the project root:

```bash
source env/Scripts/activate
python -m pytest -v
```

Tests use an isolated SQLite database and do not require the development database to be populated.

## Generating the Python SDK

Start the backend, then run:

```bash
openapi-generator-cli generate \
  -i http://127.0.0.1:8000/openapi.json \
  -g python \
  -o knowledge_sdk \
  --additional-properties=packageName=knowledge_sdk
```

Consult the generated SDK's README for installation and usage instructions specific to the generated version.

## Project Structure

```text
personal-knowledge-graph/
├── app/
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
├── alembic/
├── tests/
├── frontend/
├── knowledge_sdk/
├── main.py
├── requirements.txt
├── alembic.ini
├── seed_data.sql
├── setupdev.bat
├── runapplication.bat
└── README.md
```

## Notes

- The frontend communicates with the backend exclusively through HTTP API calls.
- Database schema changes should be managed through Alembic migrations.
- Do not commit virtual environments, dependency folders, or local database files unless explicitly required by the submission instructions.