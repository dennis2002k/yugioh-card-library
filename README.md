# Yu-Gi-Oh Card Collection API

Backend API for managing user Yu-Gi-Oh card collections.

## Overview
- Register and authenticate securely using JWT
- Search and filter cards with advanced criteria
- Manage a personal card library
- Store card–set relationships and user–card ownership
- Persist data using a relational database
- Run the application in containers
- Deploy the backend to the cloud using AWS
- Basic frontend for easy interaction and demonstration

## Features
- JWT Authentication (login / protected routes)
- Card search with multiple filters (attack, defense, level, attribute, etc.)
- User card library (add / remove / quantity tracking)
- Many-to-many relationships (Cards ↔ Sets, Users ↔ Cards)
- JSON field handling for card images, prices, and sets
- Dockerized backend
- Cloud deployment with AWS ECR and AWS Fargate
- Environment variable configuration
- Automated testing with Pytest

## Tech Stack Backend
- FastAPI
- SQLModel / SQLAlchemy
- Pydantic

## Tech Stack Frontend
- Vite-React

## Database
- MySQL (Production)
- SQLite (Testing)

## DevOps / Cloud
- Docker
- AWS ECR (Container Registry)
- AWS ECS (Fargate)
- AWS Storage (RDS, S3)

## Testing Backend
- Pytest


## Architecture
- Client -> FastAPI API -> Database
- Docker -> AWS ECR -> AWS Fargate deployment


## Public Deployment
Both Backend and Frontend are deployed on AWS Fargate amd are accessible via the puplic ips http://51.20.105.92 and http://16.170.202.2 accordingly.

### Note: The deployment currently uses HTTP (no domain / HTTPS yet).
- Future improvement includes adding HTTPS and a custom domain.
<!-- ## Setup Locally -->
<!-- ```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``` -->
## Run locally
- Create .env file with DATABASE_URL and SECRET_KEY
- RUN with Docker:
```bash 
docker compose up --build
```

## Running tests
```bash
python -m pytest
```