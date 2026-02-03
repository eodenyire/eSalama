# eSalama Schools – Data Privacy & Security

## 1. Overview

eSalama Schools handles highly sensitive information including **child locations, attendance, and personal identifiers**. This document outlines the privacy policies, security architecture, and best practices to ensure **data protection, compliance, and child safety**.

---

## 2. Key Principles

1. **Consent-Driven Data Collection**

   * GPS tracking, live streaming, and notifications are activated only with parental or guardian consent.

2. **Least Privilege Access**

   * Users (parents, teachers, admins) access only data necessary for their role.

3. **Data Minimization**

   * Only required data points are collected and retained.

4. **Transparency**

   * Parents and guardians are informed about what data is collected, how it is used, and who can access it.

5. **Security by Design**

   * Encryption, authentication, and audit logging are integral to system design.

---

## 3. Data Classification

| Data Type                  | Sensitivity | Storage        | Retention              |
| -------------------------- | ----------- | -------------- | ---------------------- |
| Student Name & ID          | High        | Relational DB  | Permanent              |
| Attendance Records         | Medium      | Relational DB  | Term / Annual          |
| GPS Coordinates            | High        | Time-Series DB | 30 days (configurable) |
| Video Streams              | High        | Object Storage | 24–48 hours            |
| Notifications Logs         | Medium      | Relational DB  | 1 year                 |
| System Logs & Audit Trails | High        | Logging DB     | 1 year                 |

---

## 4. Security Architecture

### 4.1 Network & Transport

* All communications use **TLS 1.2+**
* VPN or private network recommended for school gate devices

### 4.2 Authentication & Authorization

* **JWT Tokens** for session management
* Role-Based Access Control (RBAC)
* Device registration and authentication for student and gate devices

### 4.3 Data Encryption

* **In-Transit**: TLS/HTTPS
* **At-Rest**: AES-256 encryption for databases and object storage
* QR codes encrypted and contain **time-bound tokens** to prevent replay attacks

### 4.4 Audit & Monitoring

* Full audit logs for:

  * Attendance events
  * Device access
  * Admin activity
* Alerts for suspicious behavior (e.g., GPS tampering)

### 4.5 Offline & Resilience

* Offline QR scans buffered locally and synced securely when online
* Temporary caching for GPS data if network unavailable

---

## 5. Compliance & Regulations

* Aligns with **Kenya Data Protection Act (2019)**
* GDPR principles considered for international expansion
* Child protection regulations enforced:

  * Restricted access to sensitive data
  * Mandatory consent for tracking/streaming
  * Minimal retention policies

---

## 6. Privacy Measures

1. **Parental Control**

   * Parents can enable/disable tracking and live streams

2. **Teacher Restrictions**

   * Teachers see attendance, not full GPS streams

3. **Admin Controls**

   * Admins have system-wide access but with **audit logging**

4. **Data Retention Policies**

   * GPS: 30 days
   * Video: 24–48 hours
   * Attendance: Academic term

5. **Anonymization for Reports**

   * Aggregate analytics do not reveal individual identities unless necessary

---

## 7. Risk Mitigation

* Device Tampering: Alerts if GPS, app integrity, or QR generation is compromised
* Unauthorized Access: Multi-factor authentication for admins
* Data Breach: Encryption, audit logs, and immediate alert system
* Data Loss: Regular backups, cloud storage redundancy, disaster recovery plan

---

## 8. Recommendations

1. Conduct **annual security audits** and penetration testing
2. Update **parent and teacher privacy notices** regularly
3. Train school staff on **data protection best practices**
4. Maintain a **privacy-first culture** for all features and updates

---

*eSalama Schools – Ensuring every child’s journey is safe, secure, and private.*

