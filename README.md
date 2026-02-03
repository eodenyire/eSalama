# eSalama Schools

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**GitHub Repository:** [www.github.com/eodenyire/eSalama](https://www.github.com/eodenyire/eSalama)

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Applications](#applications)
5. [Tech Stack](#tech-stack)
6. [Installation & Setup](#installation--setup)
7. [Contributing](#contributing)
8. [License](#license)

---

## Project Overview

eSalama Schools is a **secure, real-time student tracking and communication system** designed to enhance **child safety**, streamline **school attendance management**, and provide **real-time updates to parents and teachers**.

It integrates **mobile applications, backend services, gate scanners, and an admin portal** into a unified platform.

### Objectives

* Real-time location tracking of students during school commutes
* QR code-based attendance verification at school gates
* Live notifications for parents and teachers
* Comprehensive reporting and analytics
* Secure, role-based access for all stakeholders

---

## Features

* GPS tracking every 2 minutes
* Live video streaming (optional, parent-enabled)
* QR code generation and scanning for attendance
* Real-time notifications via push, SMS, and email
* Role-based access for parents, teachers, admins
* Centralized backend portal with reporting & analytics
* Emergency/SOS alerts
* Data privacy and compliance with local regulations

---

## System Architecture

Refer to [docs/architecture.md](docs/architecture.md) for full system architecture including:

* Client applications (Student, Parent, Teacher)
* Gate scanner app
* Backend services (API Gateway, Core Services, Real-Time Hub)
* Database design (Relational, Time-Series, Object Storage)
* Notification and analytics systems
* Security and compliance framework

---

## Applications

### 1. Student App

* Runs on tablet or smartwatch
* Sends GPS coordinates and QR codes
* Optional live streaming
* Emergency alerts

### 2. Parent App

* Receives arrival, departure, and location notifications
* Optionally views live streaming
* Evening pickup reminders

### 3. Teacher App

* Receives class attendance alerts
* Sends notifications to parents
* Monitors class trends

### 4. Gate Scanner App

* Scans QR codes at school gates
* Validates student identity and timestamps
* Supports offline scanning with sync

### 5. Backend Admin Portal

* User and device management
* Attendance monitoring
* Reporting and analytics dashboards
* Security & compliance monitoring

---

## Tech Stack

### Backend (Python/FastAPI)
- **Framework**: FastAPI 0.109.2
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis
- **Authentication**: JWT (JSON Web Tokens)
- **QR Codes**: qrcode library with PIL
- **Notifications**: Twilio (SMS), AWS SES (Email)
- **API Documentation**: Automatic OpenAPI/Swagger

### Frontend (React)
- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: TanStack Query
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Maps**: React Leaflet
- **Charts**: Recharts

### Mobile Apps
- Flutter (cross-platform) or native Android/iOS (to be implemented)

### DevOps & Infrastructure
- Docker & Docker Compose
- CI/CD pipelines
- Cloud deployment (AWS/GCP/Azure)

---

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 12+
- Git

### Clone Repository
```bash
git clone https://github.com/eodenyire/eSalama.git
cd eSalama
```

### Setup Backend (Python/FastAPI)
```bash
cd backend
./setup.sh
# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration
uvicorn src.main:app --reload
```

Backend will be available at: http://localhost:8000  
API Documentation: http://localhost:8000/docs

### Setup Frontend (React)
```bash
cd admin-portal
./setup.sh
# Or manually:
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

---

## Installation & Setup

### Backend

1. Clone the repository: `git clone https://www.github.com/eodenyire/eSalama.git`
2. Navigate to backend: `cd eSalama/backend`
3. Set up environment variables (`.env`) for DB, JWT secrets, API keys
4. Run migrations and seed data
5. Start backend server using Docker/Kubernetes or locally

### Mobile Apps

1. Navigate to the respective app folder: `cd eSalama/mobile/student-app`
2. Install dependencies: `flutter pub get` (if using Flutter)
3. Configure backend API endpoint in environment config
4. Build and deploy to device or emulator

### Gate Scanner

1. Navigate to: `cd eSalama/gate-scanner`
2. Configure school ID, authentication token, and backend URL
3. Deploy to gate device

### Admin Portal

1. Navigate to: `cd eSalama/admin-portal`
2. Install dependencies: `npm install`
3. Configure environment variables for backend API
4. Start portal: `npm run dev`

---

## Contributing

We welcome contributions from developers and educational institutions.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m "Description of feature"`
4. Push branch: `git push origin feature-name`
5. Create a Pull Request

Refer to `docs/` for detailed system documentation before contributing.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

*eSalama Schools – Securing every child’s journey from home to school and back.*

