# eSalama Schools – User Roles & Permissions

## 1. Overview

eSalama Schools implements a **Role-Based Access Control (RBAC)** system to ensure that users access only the information necessary for their responsibilities while maintaining the privacy and security of student data.

Roles are defined for parents, teachers, school administrators, and system administrators.

---

## 2. Roles & Permissions

| Role   | Permissions                                            | Access Scope |
| ------ | ------------------------------------------------------ | ------------ |
| Parent | - View child attendance (arrival, departure, on route) |              |

* Receive notifications (push/SMS/email)
* Enable/disable live tracking & streaming
* Receive pickup reminders | Their own child(ren) only |
  | Class Teacher | - View class attendance dashboard
* Receive real-time arrival/departure alerts
* Send bulk notifications to parents
* View end-of-day summaries | Assigned class(es) only |
  | School Administrator | - Manage student profiles
* Manage teacher accounts
* Manage devices (student tablets, gate scanners)
* View school-wide attendance
* Access audit logs
* Generate reports | Entire school |
  | System Administrator | - Full system access
* Manage all schools, classes, devices, and accounts
* System configuration and deployment
* Security and compliance settings | Global (all schools) |

---

## 3. Access Control Principles

1. **Least Privilege**

   * Users only access data essential for their role.

2. **Segregation of Duties**

   * Teachers cannot alter student attendance outside their assigned class.
   * Parents cannot access other children’s data.

3. **Time-Bound Access**

   * Temporary roles (e.g., substitute teacher) can be assigned with expiry.

4. **Audit Logging**

   * All access and actions are logged for accountability.

5. **Device Binding**

   * Student and gate devices are registered; role access is tied to verified devices.

---

## 4. Example Scenarios

### 4.1 Arrival at School

* Student generates QR code
* Gate scanner validates
* Attendance event triggers

  * Parent receives notification
  * Teacher receives alert for assigned class
  * Admin logs event

### 4.2 Live Tracking Enabled

* Parent opts in for live tracking
* Backend streams GPS from student device
* Teacher sees aggregate status only
* Admin monitors for compliance or issues

### 4.3 Reporting Access

* Teacher: Class-level attendance and alerts
* School Admin: School-wide reports and trend analysis
* System Admin: Multi-school analytics, system health

---

## 5. Role Management & Provisioning

* Roles assigned during **account creation**
* Changes must be **approved by School Admin**
* Temporary elevated privileges can be issued with **audit logs**
* Deactivation occurs automatically when students graduate or leave

---

*eSalama Schools – Secure, role-based access for safe, accountable student journeys.*

