# Yu-Gi-Oh Card Collection API

Backend API for managing user Yu-Gi-Oh card collections.

[![Push Backend to AWS ECR/ECS](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/deploy_backend.yml/badge.svg)](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/deploy_backend.yml)
[![Push Frontend to AWS ECR/ECS](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/deploy_frontend.yml/badge.svg)](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/deploy_frontend.yml)
[![Python Tests](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/tests.yml/badge.svg)](https://github.com/dennis2002k/yugioh-card-library/actions/workflows/tests.yml)

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
- DevOps: GitHub Actions (Automated CI/CD Pipeline)

## Testing Backend
- Pytest


## Architecture
- Client -> FastAPI API -> Database
- Docker -> AWS ECR -> AWS Fargate deployment


## Public Deployment
Both Backend and Frontend are deployed on AWS Fargate amd are accessible via the puplic ips http://16.171.197.197:8000/docs and http://16.171.159.38 accordingly.

### Note: The deployment currently uses HTTP (no domain / HTTPS yet).
- Future improvement includes adding HTTPS and a custom domain.
<!-- ## Setup Locally -->
<!-- ```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``` -->
## Run locally

### RUN with Docker:
- Create .env file with DATABASE_URL(mysql+pymysql://user:password@db:3306/ygo_db to use the one created by the docker-compose), SEED_DATABASE_URL(mysql+pymysql://user:password@127.0.0.1:3306/ygo_db) to seed cards to database and SECRET_KEY(openssl rand -hex 32 to create a random one)
- Create .env.production inside the /frontend folder with VITE_API_URL (http://localhost:8000) and VITE_S3_URL(https://ygo-cards-images-dennis2002k.s3.eu-north-1.amazonaws.com/) for the frontend to show images.  

- RUN to get cards into database
```bash
python -m scripts.seed_cards
```

```bash 
docker compose up --build
```

### RUN without docker

- Setup
1. 
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Inside /frontend
```bash
npm install
```

3. Create a database or use "sqlite:///:memory:" as DATABASE_URL for a in memory database.

4.  Create .env file with DATABASE_URL, SEED_DATABASE_URL to seed cards to database and SECRET_KEY(openssl rand -hex 32 to create a random one)
- Create .env.development inside the /frontend folder with VITE_API_URL (http://16.171.197.197:8000) and VITE_S3_URL(https://ygo-cards-images-dennis2002k.s3.eu-north-1.amazonaws.com/) for the frontend to show images.

5. RUN to get cards into database
```bash
python -m scripts.seed_cards
```

6. RUN Backend
```bash
python -m fastapi dev app/app.py
```
7. RUN Frontend inside /frontend
```bash
npm run dev
```

## Running tests
```bash
python -m pytest
```