# Hazard‑Assessment-Workflow API
A lightweight FastAPI-based application to capture and manage risks with automated background workflows, task assignment, and database persistence using SQLite. Includes CI/CD via GitHub Actions and Docker support.

---
A tiny FastAPI service that tracks **risks** and spawns follow‑up **tasks** automatically in a background job.

hazard-workflow/  
├── app/  
│ ├── main.py # FastAPI entry point  
│ ├── schemas.py # Pydantic request/response models  
│ ├── database.py # SQLite engine & table definitions  
│ └── init.py  
├── tests/  
│ ├── test_api.py # Unit tests using pytest  
│ └── init.py  
├── requirements.txt # Python dependencies  
├── Dockerfile # Docker image definition  
├── README.md # Project documentation  
└── .github/  
    └── workflows/  
        └── test.yml # GitHub Actions CI pipeline
        
## Requirements
- Implement a REST API (with FastAPI) with the following endpoints:
  - POST /risks - captures a new risk (title, description, category) and starts the workflow
  - GET /risks - lists all risks with their current status
  - GET /risks/{id} - returns the details of a specific risk and the status

- Workflow logic:
  - Create automatic tasks for "safety officer" and "team leader"
  - Initially set status to "in process"
  - Simulate processing for 10 seconds
  - Then set status to "completed"
    
- Data storage: Use either SQLite
- Unit tests for the endpoints
- A Dockerfile for the local start  
  
## Git Command
-The git command to execute the code is below under >>> Quick start (local) >>>

Then visit: http://localhost:8000/docs

### NOTES: Python version 3.12.6

## Running with Docker 
1. Build the Docker image
docker build -t hazard-api 

2. Run the container
docker run -p 8000:80 hazard-api

## UI:
![Screenshot of a FASTAPI.](SwaggerUI.png)

## CI/CD pipeline setup
- This project uses GitHub Actions to automate the CI/CD pipeline for building, testing, and deploying the application Docker image.

### Workflow Overview
The pipeline is defined in .github/workflows/test.yml and triggers on:
- Pushes to the main branch
- Pull requests targeting the main branch

#### Pipeline Jobs
Build & Test
- Runs on ubuntu-latest
- Checks out the code
- Sets up Python 3.11
- Installs dependencies from requirements.txt
- Runs unit tests using pytest
- Docker Build & Push
- Runs only if the build job succeeds and the branch is main
- Checks out the code again
- Sets up Docker Buildx for multi-platform builds
- Logs in to Docker Hub using repository secrets (DOCKER_USERNAME and DOCKER_PASSWORD)
- Builds the Docker image and pushes it to Docker Hub with the tag latest

#### Branch Naming
- Ensure your main development branch is named main or update the workflow file accordingly.

### Testing
- Write tests under the tests/ directory. The workflow runs tests automatically on every push and pull request.

#### How to Trigger the Pipeline
- Push changes to the main branch.
- Open a pull request targeting main.

## Deployment
- Use Docker in combination with Kubernetes for advanced orchestration

## CI/CD with GitHub Actions
- Included .github/workflows/test.yml handles:
- Build & dependency setup
- Unit test execution with pytest
- Docker build & push to DockerHub (when secrets are configured)

## Extending the App
- Add more roles or task types in schemas.py and update _workflow_create_tasks.
- Add endpoints to update task status or assign users.
- Replace SQLite with PostgreSQL for multi-user production.

## Scaling in Production
- Here’s how you could scale this app beyond a prototype:

## Replace BackgroundTasks
- Use Celery or RQ as a distributed task queue for workflows.

## Database
- Switch from SQLite to PostgreSQL or MySQL.
- Use Alembic for database migrations.

  ## Quick start (local)

```bash
python -m venv .venv 
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
pytest tests/test_api.py ```   ###testing the api 

### Thank you :) 
