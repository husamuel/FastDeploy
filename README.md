# 📌 FastDeploy — Speed: Launch Product Faster

## 🎯 Objective
Reduce the launch time for new features, minimizing time-to-market and accelerating value delivery to customers.

## 🚀 Technical Implementation
- Developed a simple **Python (FastAPI)** API for product registration.
- Configured **CI/CD** in **GitHub Actions**:
  - Each push triggers automated tests.
  - If tests pass, a **Docker** image is generated.
  - Automatic deployment to **Heroku** (or local **Kubernetes**).
- Used **Docker** to ensure the application runs consistently across environments.
- Created basic unit tests to validate critical API functionalities.

## 💡 Value Delivered
- **Faster**: Each commit goes to production automatically.
- **More Reliable**: Tests prevent bugs from reaching production.
- **Less Manual Effort**: Automated build and deployment reduce rework.

## 📊 Impact Metrics
- Lead time for delivery reduced from 2 days to 10 minutes.
- Rapid feedback for developers, enabling immediate fixes.
- Demonstrates continuous delivery and automation as real business value.

## 🛠️ Tech Stack
- **Language & Framework**: Python, FastAPI
- **Containers & Orchestration**: Docker
- **CI/CD**: GitHub Actions
- **Deployment**: Heroku or local Kubernetes
- **Testing**: Pytest
- **Monitoring**: Optionally Grafana / centralized logs

## 📂 Project Structure
