# eSalama Schools – Reporting & Analytics

## 1. Overview

eSalama Schools provides advanced reporting and analytics to give administrators, teachers, and parents insights into **attendance trends, student safety, and operational performance**. Reports are generated from both historical and real-time data.

---

## 2. Key Reporting Modules

### 2.1 Attendance Reports

* Daily, weekly, term-wise attendance
* Class-level and school-level summaries
* Late arrivals, early departures, absences
* Export options: CSV, Excel, PDF

### 2.2 Location & Route Reports

* GPS trails of student journeys
* Geo-fence entry/exit verification
* Heatmaps for route density
* Alerts for deviations or anomalies

### 2.3 Notification Reports

* Delivered notifications per student or class
* Read receipts for parents and teachers
* Failed or retried notifications

### 2.4 Safety & Incident Reports

* SOS triggers and response times
* Video or snapshot audit events
* Compliance with retention policies

### 2.5 Aggregate Analytics

* Student attendance trends over time
* Class or grade comparisons
* Parent engagement metrics
* Device usage patterns

---

## 3. Reporting Features

* **Role-based access**: Admins see full school data, teachers see class-level data, parents see their child only
* **Custom date ranges**: Daily, weekly, term, or custom range selection
* **Automated generation**: Schedule reports to be emailed or pushed to dashboards
* **Visualizations**: Graphs, charts, and heatmaps for quick insight
* **Audit logs**: All generated reports are logged for accountability

---

## 4. Example Reports

### 4.1 Daily Attendance Summary

| Student           | Arrival | Departure | Status  |
| ----------------- | ------- | --------- | ------- |
| Emmanuel Odenyire | 06:53   | 16:45     | Present |
| Jane Mwangi       | 06:58   | 16:50     | Present |

### 4.2 Weekly Attendance Trends (Class Form 4 Blue)

* Average attendance: 96%
* Students with repeated late arrivals: 3

### 4.3 Route Safety Heatmap

* Map showing concentration of GPS locations along common routes
* Alerts flagged for students deviating from expected path

### 4.4 Notification Summary

* Arrival notifications sent: 150
* Read confirmations: 145
* SMS fallback triggered: 5

---

## 5. Data Sources

* Attendance service logs
* GPS location service (time-series DB)
* QR code verification events
* Notification service logs
* Admin portal inputs

---

## 6. Security & Privacy in Reporting

* Data anonymization for aggregated analytics
* Role-based visibility enforced at query level
* Encrypted exports for sensitive data
* Retention policies applied to historical data

---

*eSalama Schools – Insights and analytics to keep every child’s journey visible, safe, and accountable.*

