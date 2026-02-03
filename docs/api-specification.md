# eSalama Schools – API Specification

## 1. Overview

eSalama Schools backend exposes **RESTful APIs** (with optional GraphQL in v2) to handle student tracking, attendance, notifications, and administrative functions. All APIs require **authenticated access** and follow **role-based access control**.

All timestamps are **UTC**, and all payloads containing sensitive data are **encrypted in transit**.

---

## 2. Authentication

### 2.1 Login

```
POST /api/auth/login
```

**Request:**

```json
{
  "email": "user@example.com",
  "password": "securePassword"
}
```

**Response:**

```json
{
  "token": "<JWT_TOKEN>",
  "role": "parent|teacher|admin|system_admin",
  "expires_in": 3600
}
```

### 2.2 Token Refresh

```
POST /api/auth/refresh
```

Request: `refresh_token`
Response: New JWT token

---

## 3. Student APIs

### 3.1 Get Student Profile

```
GET /api/students/{studentId}
```

**Permissions:** Parent (own child), Teacher (assigned class), Admin (school)
**Response:**

```json
{
  "id": "IF2811",
  "name": "Emmanuel Odenyire",
  "class": "Form 4 Blue",
  "device_id": "DEVICE123"
}
```

### 3.2 Update Device Info

```
PUT /api/students/{studentId}/device
```

Payload:

```json
{
  "device_id": "NEWDEVICE123",
  "device_type": "tablet|watch"
}
```

**Permissions:** Admin only

---

## 4. Attendance APIs

### 4.1 Record Arrival / Departure

```
POST /api/attendance
```

Payload:

```json
{
  "student_id": "IF2811",
  "type": "arrival|departure",
  "timestamp": "2026-02-03T06:53:00Z",
  "location": {
    "lat": -1.28333,
    "lng": 36.81667
  },
  "qr_code_token": "TOKEN123"
}
```

**Response:** 200 OK
**Permissions:** Gate Scanner, Admin, Student Device (QR)

### 4.2 Get Attendance

```
GET /api/attendance?studentId=IF2811&date=2026-02-03
```

Response:

```json
[
  {"type": "arrival", "time": "06:53"},
  {"type": "departure", "time": "16:45"}
]
```

**Permissions:** Parent (own child), Teacher (class), Admin (school)

---

## 5. Location APIs

### 5.1 Post GPS Coordinates

```
POST /api/location
```

Payload:

```json
{
  "student_id": "IF2811",
  "timestamp": "2026-02-03T06:55:00Z",
  "location": {"lat": -1.28333, "lng": 36.81667}
}
```

**Permissions:** Student Device

### 5.2 Get Last Known Location

```
GET /api/location/{studentId}/last
```

Response:

```json
{
  "timestamp": "2026-02-03T06:55:00Z",
  "lat": -1.28333,
  "lng": 36.81667
}
```

**Permissions:** Parent, Teacher, Admin

---

## 6. QR Code APIs

### 6.1 Generate QR Code

```
POST /api/qr/generate
```

Payload:

```json
{
  "student_id": "IF2811",
  "type": "arrival|departure"
}
```

Response:

```json
{
  "qr_code_url": "https://.../qr/IF2811_ARRIVAL.png",
  "token": "TOKEN123"
}
```

**Permissions:** Student Device

### 6.2 Validate QR Code

```
POST /api/qr/validate
```

Payload:

```json
{
  "token": "TOKEN123",
  "scanner_id": "GATE1"
}
```

Response: 200 OK or 401 Unauthorized
**Permissions:** Gate Scanner, Admin

---

## 7. Notification APIs

### 7.1 Send Notification

```
POST /api/notifications
```

Payload:

```json
{
  "recipient_role": "parent|teacher",
  "student_id": "IF2811",
  "type": "arrival|departure|alert",
  "message": "Your child has arrived at school at 06:53AM"
}
```

**Permissions:** System, Admin, Gate Scanner

### 7.2 Get Notification History

```
GET /api/notifications?studentId=IF2811
```

Response: List of notifications sent
**Permissions:** Parent, Teacher, Admin

---

## 8. Reporting APIs

* `/api/reports/attendance?schoolId=123&date=2026-02-03`
* `/api/reports/gps-paths?studentId=IF2811&date=2026-02-03`
* `/api/reports/alerts?schoolId=123&dateRange=2026-02-01:2026-02-03`

**Permissions:** Admin, System Admin

---

## 9. Security Considerations

* All requests require JWT authentication
* Role-based access enforced for each endpoint
* All sensitive payloads are encrypted in transit
* Rate limiting for GPS streaming endpoints
* QR tokens are single-use and time-bound

---

*eSalama Schools – Secure, real-time API framework for student safety and attendance.*
