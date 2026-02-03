# eSalama Schools – System Architecture

## 1. Architecture Overview

eSalama Schools follows a **multi-tier, event-driven architecture** designed for reliability, scalability, and real-time responsiveness. The system separates **device-level concerns**, **application logic**, and **data processing** while enforcing strict security and access controls.

At a high level, the platform consists of:

* Edge devices (student devices and gate scanners)
* Client applications (mobile and web)
* Backend services (APIs, real-time services)
* Data and analytics infrastructure
* Notification and integration services

---

## 2. High-Level Architecture Diagram (Logical)

```
+-------------------+        +-------------------+
| Student Device    |        | Gate Scanner      |
| (Tablet/Watch)   |        | (QR Scanner App)  |
+---------+---------+        +---------+---------+
          |                            |
          | GPS / QR / Stream          | QR Scan Events
          |                            |
          v                            v
+--------------------------------------------------+
|              Backend API Gateway                 |
+----------------+----------------+----------------+
                 |                |
        +--------v----+   +-------v-------+
        | Core APIs   |   | Real-Time Hub  |
        | (REST)      |   | (WebSockets)  |
        +--------+----+   +-------+-------+
                 |                |
        +--------v----------------v----------------+
        |        Application Services                |
        | Auth | Attendance | Location | QR | Logs |
        +--------+----------------+----------------+
                 |                |
      +----------v---+     +------v----------------+
      | Databases    |     | Notification Services |
      | (SQL/TS)     |     | Push | SMS | Email    |
      +--------------+     +-----------------------+
                 |
        +--------v------------------+
        | Admin Portal & Reports    |
        +---------------------------+
```

---

## 3. Client-Side Architecture

### 3.1 Student Application

Responsibilities:

* Periodic GPS capture and transmission
* QR code generation (arrival/departure)
* Live video streaming (on-demand)
* Geo-fence detection
* Emergency/SOS triggers

Design considerations:

* Battery-efficient background services
* Offline buffering and delayed sync
* Device authentication and integrity checks

---

### 3.2 Parent Application

Responsibilities:

* Display real-time student status
* Receive notifications
* Enable or disable live tracking/streaming
* View historical attendance summaries

Privacy controls are enforced at the API level to ensure parents only access their own child’s data.

---

### 3.3 Class Teacher Application

Responsibilities:

* View class attendance status
* Receive arrival and departure alerts
* Send bulk notifications to parents

Teachers interact only with **attendance events**, not raw location streams.

---

### 3.4 Gate Scanner Application

Responsibilities:

* Scan and decode encrypted QR codes
* Validate scan location (geo-fence)
* Transmit attendance events
* Support offline scanning with later synchronization

Gate devices are **registered and whitelisted** in the backend.

---

## 4. Backend Architecture

### 4.1 API Gateway Layer

* Single entry point for all client requests
* Handles authentication, rate limiting, and logging
* Routes requests to internal services

---

### 4.2 Core Application Services

| Service                | Responsibility                      |
| ---------------------- | ----------------------------------- |
| Authentication Service | User identity, JWT tokens, roles    |
| Student Service        | Student profiles and device linkage |
| Attendance Service     | Arrival and departure records       |
| Location Service       | GPS ingestion, geo-fencing          |
| QR Verification        | Token validation and anti-replay    |
| Notification Service   | Event-based notifications           |
| Audit Service          | Logs and compliance trails          |

Services communicate internally via synchronous APIs and asynchronous events.

---

### 4.3 Real-Time Services

Used for:

* Live location streaming
* Live video feeds
* Instant attendance updates

Technologies:

* WebSockets or MQTT
* Event queues for scalability

---

## 5. Data Architecture

### 5.1 Databases

* **Relational Database (PostgreSQL)**

  * Users
  * Students
  * Schools
  * Attendance records

* **Time-Series Database**

  * GPS coordinates
  * Movement events

* **Object Storage**

  * Temporary video streams
  * Evidence snapshots

---

### 5.2 Data Flow Principles

* All timestamps are server-generated
* Sensitive identifiers are tokenized
* Video and location data have limited retention

---

## 6. Notification Architecture

Notifications are triggered by **events**, not polling.

Examples:

* QR scan event → attendance update → notifications
* Geo-fence entry → arrival alert
* Departure scan → parent notification

Channels:

* Push notifications
* SMS (fallback)
* Email (administrative)

---

## 7. Security Architecture (Summary)

* TLS encryption for all traffic
* End-to-end encryption for sensitive payloads
* Role-based access control
* Device-level authentication
* Full audit logging

(See `data-privacy-security.md` for full details.)

---

## 8. Scalability & Availability

* Stateless backend services
* Horizontal scaling via containers
* Load balancers and auto-scaling
* Caching for high-frequency reads

Designed to support:

* Single-school deployments
* Multi-school and county-level rollouts

---

## 9. Integration & Extensibility

Future integrations may include:

* School ERP systems
* Bus tracking systems
* National education databases
* Identity verification services

---

## 10. Summary

eSalama Schools’ architecture ensures **real-time visibility, secure attendance verification, and strong privacy protections**, while remaining flexible enough to scale across institutions and regions.

