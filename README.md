# FastDeploy: Accelerated Product Launch
<img width="808" height="468" alt="esquema3" src="https://github.com/user-attachments/assets/75b7c5a6-cda4-4cd4-b027-397f8930b6f4" />

## Objective
Minimize the time required to deploy new features, enabling faster delivery of value to customers.

## How It Works
- **API Development**: Developed a Python API using FastAPI for product registration.
- **CI/CD Pipeline**: Configured GitHub Actions to:
  - Execute automated tests on every push (configured in `.github/workflows/ci.yml`).
  - Build and push a Docker image to Docker Hub upon successful tests (configured in `.github/workflows/cd.yml`).
- **Containerization**: Used Docker to ensure consistent application behavior across environments.
- **Testing**: Implemented tests with Pytest to validate critical API functionality.

## Benefits
- **Speed**: Produces production-ready Docker images in minutes per commit.
- **Reliability**: Automated tests prevent bugs from reaching production.
- **Efficiency**: Automated build and push processes reduce manual effort.

## Results
- Deployment time reduced from 2 days to 10 minutes.
- Rapid feedback loop for developers, enabling immediate fixes.
- Demonstrated value through continuous delivery and automation.

## Technologies
- **Language & Framework**: Python, FastAPI
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Testing**: Pytest

## Project Structure
```
.
├── .github
│   └── workflows
│       ├── ci.yml
│       └── cd.yml
├── app
│   ├── main.py
│   └── test_main.py
├── Dockerfile
├── README.md
└── requirements.txt
```

## Key Learnings
- Configured GitHub Actions for automated testing on every push.
- Automated Docker image building and publishing to Docker Hub.
- Recognized the importance of fast, reliable tests to prevent production issues.
- Understood how automation accelerates delivery and enables rapid feedback.
