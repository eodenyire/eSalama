# eSalama Schools – Notification Flows

## 1. Overview

Notifications in eSalama Schools are **event-driven** and aim to provide real-time alerts for parents, teachers, and administrators while preserving privacy and minimizing unnecessary messages.

Notification events include:

* Student arrival at school
* Student departure from school
* On-route updates
* Emergency/SOS events
* Evening pickup reminders

---

## 2. Notification Flow Diagrams

### 2.1 Student Arrival

```
[Student Device] --QR Generated--> [Gate Scanner]
[Gate Scanner] --Validate QR--> [Backend]
[Backend] --Push Notification--> [Parent App]
[Backend] --Push Notification--> [Teacher App]
[Backend] --Record Event--> [Admin Portal]
```

### 2.2 Student Departure

```
[Student Device] --QR Generated--> [Gate Scanner]
[Gate Scanner] --Validate QR--> [Backend]
[Backend] --Push Notification--> [Parent App]
[Backend] --Push Notification--> [Teacher App]
[Backend] --Record Event--> [Admin Portal]
```

### 2.3 On-Route Updates (Every 2 Minutes)

```
[Student Device] --GPS Update--> [Backend]
[Backend] --Optional Push--> [Parent App]
[Backend] --Store GPS Data--> [Database]
```

### 2.4 Live Streaming (Optional)

```
[Student Device] --Stream--> [Real-Time Service]
[Real-Time Service] --Secure Stream--> [Parent App]
[Real-Time Service] --Monitor--> [Admin Portal]
```

### 2.5 Evening Pickup Reminder (For Younger Students)

```
[Backend Scheduler] --Time Trigger--> [Parent App]
Message: "Evening pickup reminder: Your child Emmanuel Odenyire should be collected soon."
```

---

## 3. Notification Channels

* **In-app push notifications** (primary)
* **SMS** (fallback for low-connectivity regions)
* **Email** (administrative summary or alerts)

---

## 4. Event-to-Notification Mapping

| Event Type       | Recipient | Channel    | Message Example                                                    |
| ---------------- | --------- | ---------- | ------------------------------------------------------------------ |
| Arrival          | Parent    | Push/SMS   | "Good morning, Emmanuel Odenyire has arrived at school at 06:53AM" |
| Arrival          | Teacher   | Push       | "Student Emmanuel Odenyire (Form 4 Blue) has arrived"              |
| Departure        | Parent    | Push/SMS   | "Emmanuel Odenyire has left the school at 04:45PM"                 |
| On-Route         | Parent    | Push       | "Emmanuel Odenyire is 500m from school gate"                       |
| SOS              | Parent    | Push/SMS   | "Emergency alert: Emmanuel Odenyire triggered SOS at 07:30AM"      |
| SOS              | Admin     | Push/Email | "Emergency alert triggered by IF2811, immediate response required" |
| Evening Reminder | Parent    | Push       | "Evening pickup reminder for Emmanuel Odenyire"                    |

---

## 5. Notification Rules

1. Notifications are **role-specific**; parents do not see other students’ updates.
2. **Throttling**: Limit high-frequency updates (GPS/streaming) to avoid notification overload.
3. **Retry Mechanism**: For failed deliveries (SMS or push), retries occur within 5 minutes.
4. **Audit Logs**: Every notification event is logged for compliance and troubleshooting.

---

*eSalama Schools – Timely, secure, and role-specific notifications for student safety.*

