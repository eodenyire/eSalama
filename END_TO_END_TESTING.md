# eSalama End-to-End Testing Guide

Complete testing guide to verify the entire eSalama system works from sending alerts and notifications to parents, teachers, and backend, to scanning QR codes, reporting, and all system components.

## System Overview

The eSalama system consists of:
1. **Backend API** (Python/FastAPI) - Core services
2. **Admin Portal** (React) - Web dashboard
3. **Gate Scanner** (Android) - QR code scanning
4. **Student App** (React Native) - QR generation & GPS tracking
5. **Parent App** (React Native) - Notifications & tracking
6. **Teacher App** (React Native) - Attendance & notifications

---

## Prerequisites

### Backend Setup
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```
Backend running at: http://localhost:8000

### Verify Backend Health
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

### Create Test Accounts
```bash
# Create Admin User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123",
    "full_name": "Test Admin",
    "role": "admin"
  }'

# Create Parent User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "parent@test.com",
    "password": "parent123",
    "full_name": "Test Parent",
    "phone": "+254712345678",
    "role": "parent"
  }'

# Create Teacher User
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "teacher@test.com",
    "password": "teacher123",
    "full_name": "Test Teacher",
    "role": "teacher"
  }'

# Create Student User (for the app)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@test.com",
    "password": "student123",
    "full_name": "Test Student",
    "role": "parent"
  }'
```

### Create Student Record
```bash
# Login as admin first to get token
ADMIN_TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@test.com&password=admin123" | jq -r '.access_token')

# Create student
curl -X POST http://localhost:8000/api/v1/students \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "STU001",
    "full_name": "John Doe",
    "class_name": "Grade 5A",
    "school_id": 1,
    "parent_id": 2,
    "device_type": "tablet"
  }'
```

---

## Test Scenario 1: Morning Arrival Flow

### Step 1: Student Opens App
1. Launch Student App on mobile/emulator
2. Login with: `student@test.com` / `student123`
3. **Verify**: Home screen loads with QR code
4. **Verify**: GPS tracking status shows "Active"
5. **Verify**: Countdown timer displays time until QR expiry

### Step 2: Generate QR Code
**Expected API Call:**
```
POST /api/v1/qr/generate
{
  "student_id": 1,
  "attendance_type": "arrival"
}
```

**Verify in Backend Logs:**
```bash
# Check backend logs for QR generation
# Should see: "QR code generated for student 1"
```

**Verify QR Code:**
- QR displays on screen
- Format: `{student_id}|{attendance_type}|{token}`
- Token is 32 characters
- Expiry countdown starts from 15:00

### Step 3: Scan QR at Gate
1. Open Gate Scanner app (Android)
2. Login with gate scanner credentials
3. Point camera at Student App QR code
4. **Verify**: Scanner reads QR code automatically
5. **Verify**: Success message displays
6. **Verify**: Student name shown

**Expected API Call:**
```
POST /api/v1/qr/validate
{
  "token": "abc123..."
}

POST /api/v1/attendance
{
  "student_id": 1,
  "type": "arrival",
  "timestamp": "2024-01-15T08:30:00Z",
  "latitude": -1.2345,
  "longitude": 36.7890,
  "scanner_id": "main_gate_scanner"
}

POST /api/v1/notifications (automatic)
{
  "student_id": 1,
  "type": "arrival",
  "message": "Good morning, John Doe has safely entered..."
}
```

### Step 4: Parent Receives Notification
1. Open Parent App
2. **Verify**: New notification appears in dashboard
3. **Verify**: Message: "Good morning, John Doe has safely entered the school gate at 08:30 AM"
4. **Verify**: Notification marked as unread (blue dot)
5. Tap notification to mark as read
6. **Verify**: Dot disappears

**Backend Query:**
```bash
curl http://localhost:8000/api/v1/notifications \
  -H "Authorization: Bearer $PARENT_TOKEN"
```

### Step 5: Teacher Sees Attendance
1. Open Teacher App
2. Go to Attendance tab
3. **Verify**: John Doe appears in list
4. **Verify**: Badge shows "ARRIVAL" in green
5. **Verify**: Time shows 08:30 AM
6. **Verify**: Location coordinates displayed

**Backend Query:**
```bash
curl http://localhost:8000/api/v1/attendance?date=2024-01-15 \
  -H "Authorization: Bearer $TEACHER_TOKEN"
```

### Step 6: Admin Portal Updates
1. Open Admin Portal (http://localhost:3000)
2. Login with admin credentials
3. Go to Dashboard
4. **Verify**: Total arrivals count incremented
5. Go to Attendance page
6. **Verify**: John Doe listed with arrival time
7. **Verify**: Real-time update (if WebSocket enabled)

---

## Test Scenario 2: GPS Location Tracking

### Step 1: Student App Tracks Location
With Student App running:
1. **Verify**: Status shows "Location Tracking Active"
2. Wait 2 minutes
3. **Verify**: Location posted to backend

**Expected API Call (every 2 minutes):**
```
POST /api/v1/location
{
  "student_id": 1,
  "latitude": -1.2345,
  "longitude": 36.7890,
  "accuracy": 10.5,
  "timestamp": "2024-01-15T08:32:00Z"
}
```

**Verify in Backend:**
```bash
# Get last location
curl http://localhost:8000/api/v1/location/1/last \
  -H "Authorization: Bearer $PARENT_TOKEN"

# Expected response
{
  "id": 1,
  "student_id": 1,
  "latitude": -1.2345,
  "longitude": 36.7890,
  "accuracy": 10.5,
  "timestamp": "2024-01-15T08:32:00Z"
}
```

### Step 2: Parent Views Location on Map
1. Open Parent App
2. Go to "Track" tab
3. **Verify**: Map displays with student's location
4. **Verify**: Blue marker shows current position
5. **Verify**: "Last Update" time is recent
6. **Verify**: Accuracy shown (e.g., "±10m")
7. Tap "Refresh Location"
8. **Verify**: Map updates with new position

### Step 3: View Location History
With multiple location points posted:
1. **Verify**: Blue trail (polyline) shows path
2. **Verify**: Trail connects location points
3. **Verify**: Most recent point is at marker

**Backend Query:**
```bash
curl http://localhost:8000/api/v1/location/1/history?limit=50 \
  -H "Authorization: Bearer $PARENT_TOKEN"
```

---

## Test Scenario 3: Teacher-Parent Communication

### Step 1: Teacher Sends Notification
1. Open Teacher App
2. Go to "Notify" tab
3. Tap on "John Doe" to select
4. **Verify**: Student button highlights in orange
5. Type message: "Please bring art supplies tomorrow"
6. Tap "Send Notification"
7. **Verify**: Success message appears
8. **Verify**: Notification appears in history

**Expected API Call:**
```
POST /api/v1/notifications
{
  "student_id": 1,
  "type": "teacher_message",
  "message": "Please bring art supplies tomorrow"
}
```

### Step 2: Parent Receives Message
1. Open Parent App
2. Go to "Notifications" tab
3. **Verify**: New notification from teacher appears
4. **Verify**: Message content matches
5. **Verify**: Unread indicator shows
6. Tap notification
7. **Verify**: Marked as read

### Step 3: Verify in Backend
```bash
# List all notifications
curl http://localhost:8000/api/v1/notifications \
  -H "Authorization: Bearer $PARENT_TOKEN"

# Check notification details
curl http://localhost:8000/api/v1/notifications/1 \
  -H "Authorization: Bearer $PARENT_TOKEN"
```

---

## Test Scenario 4: Emergency SOS Alert

### Step 1: Student Triggers SOS
1. Open Student App
2. Tap "🚨 SOS EMERGENCY" button
3. **Verify**: Confirmation dialog appears
4. Tap "Send Alert"
5. **Verify**: Success message: "Emergency alert sent"

**Expected API Call:**
```
POST /api/v1/notifications
{
  "student_id": 1,
  "type": "sos",
  "message": "EMERGENCY: SOS alert from John Doe"
}
```

### Step 2: All Stakeholders Notified
1. **Parent App**: Receives high-priority notification
2. **Teacher App**: Receives emergency notification
3. **Admin Portal**: Shows emergency alert

### Step 3: Verify Alert Priority
```bash
# Get emergency notifications
curl http://localhost:8000/api/v1/notifications?type=sos \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

---

## Test Scenario 5: Afternoon Departure

### Step 1: Generate Departure QR
1. Student App still running
2. **Note**: QR code should auto-switch to "departure" type after school hours
   - Or manually test by regenerating

### Step 2: Scan at Gate on Exit
1. Gate Scanner scans departure QR
2. **Verify**: "DEPARTURE" recorded
3. **Verify**: Parent notified: "John Doe has left the school at 15:30"

**Expected API Call:**
```
POST /api/v1/attendance
{
  "student_id": 1,
  "type": "departure",
  "timestamp": "2024-01-15T15:30:00Z",
  ...
}
```

### Step 3: Verify Full Day Record
```bash
# Get attendance for the day
curl http://localhost:8000/api/v1/attendance?student_id=1&date=2024-01-15 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Expected: 2 records (arrival + departure)
```

---

## Test Scenario 6: Reports & Analytics

### Step 1: Generate Attendance Report
```bash
# Attendance report
curl http://localhost:8000/api/v1/reports/attendance?date=2024-01-15 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Expected: List of all attendance records for the day
```

### Step 2: GPS Path Report
```bash
# GPS path for student
curl http://localhost:8000/api/v1/reports/gps-paths?student_id=1&date=2024-01-15 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Expected: Array of location points
```

### Step 3: Alerts Report
```bash
# Alerts report
curl http://localhost:8000/api/v1/reports/alerts?student_id=1 \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# Expected: All notifications/alerts
```

### Step 4: View in Admin Portal
1. Open Admin Portal
2. Go to Reports section
3. Select "Attendance Report"
4. Filter by date
5. **Verify**: All records display
6. **Verify**: Charts/graphs show data
7. Export report (if implemented)

---

## Test Scenario 7: Real-Time WebSocket Updates

### Step 1: Connect to Location Stream
```javascript
// JavaScript example
const ws = new WebSocket('ws://localhost:8000/api/v1/streaming/location/1?token=JWT_TOKEN');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Location update:', data);
};
```

### Step 2: Verify Updates
1. Student App posts new location
2. **Verify**: WebSocket receives update immediately
3. **Verify**: Parent App map updates automatically

### Step 3: Notifications Stream
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/streaming/notifications?token=JWT_TOKEN');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('New notification:', data);
};
```

---

## Automated Testing Commands

### Backend API Tests
```bash
cd backend

# Test authentication
python -c "import requests; r = requests.post('http://localhost:8000/api/v1/auth/login', data={'username': 'admin@test.com', 'password': 'admin123'}); print('✓ Auth OK' if r.status_code == 200 else '✗ Auth FAIL')"

# Test health
python -c "import requests; r = requests.get('http://localhost:8000/health'); print('✓ Health OK' if r.json()['status'] == 'healthy' else '✗ Health FAIL')"

# Test QR generation
python -c "
import requests
token = requests.post('http://localhost:8000/api/v1/auth/login', data={'username': 'admin@test.com', 'password': 'admin123'}).json()['access_token']
r = requests.post('http://localhost:8000/api/v1/qr/generate', json={'student_id': 1, 'attendance_type': 'arrival'}, headers={'Authorization': f'Bearer {token}'})
print('✓ QR OK' if r.status_code == 200 else '✗ QR FAIL')
"
```

### Mobile App Tests
```bash
# Install and run Student App
cd mobile/student-app
npm install
npm run android # or ios

# Install and run Parent App
cd mobile/parent-app
npm install
npm run android # or ios

# Install and run Teacher App
cd mobile/teacher-app
npm install
npm run android # or ios
```

---

## Verification Checklist

### Backend
- [ ] Backend starts without errors
- [ ] Health check passes
- [ ] Database connected
- [ ] All API endpoints respond
- [ ] Authentication works
- [ ] JWT tokens generated

### Student App
- [ ] App installs successfully
- [ ] Login works
- [ ] QR code generates
- [ ] QR code auto-refreshes
- [ ] GPS tracking starts
- [ ] Location posts every 2 minutes
- [ ] SOS alert sends

### Parent App
- [ ] App installs successfully
- [ ] Login works
- [ ] Notifications display
- [ ] Map shows location
- [ ] Location history shows trail
- [ ] Pull-to-refresh works
- [ ] Mark as read works

### Teacher App
- [ ] App installs successfully
- [ ] Login works
- [ ] Attendance displays
- [ ] Student selection works
- [ ] Notification sends
- [ ] History displays

### Gate Scanner
- [ ] App installs successfully
- [ ] Login works
- [ ] Camera opens
- [ ] QR scanning works
- [ ] Validation successful
- [ ] Attendance recorded
- [ ] Notifications sent

### Admin Portal
- [ ] Portal loads
- [ ] Login works
- [ ] Dashboard displays data
- [ ] Students page works
- [ ] Attendance page works
- [ ] Reports generate
- [ ] Real-time updates work

### End-to-End Flows
- [ ] Full attendance flow works (Student → Scanner → Backend → Parent/Teacher)
- [ ] Location tracking works (Student → Backend → Parent)
- [ ] Communication works (Teacher → Backend → Parent)
- [ ] Emergency alerts work (Student → All Stakeholders)
- [ ] Reports generate correctly

---

## Troubleshooting

### Backend Not Starting
```bash
# Check Python version
python --version  # Should be 3.9+

# Check dependencies
pip list | grep -E "(fastapi|uvicorn)"

# Check database
psql -U postgres -c "SELECT 1"

# Check logs
tail -f backend/logs/app.log
```

### Mobile Apps Not Connecting
```bash
# Check API URL in config
cat mobile/student-app/src/config/api.js

# For emulator, use:
# Android: http://10.0.2.2:8000
# iOS: http://localhost:8000

# For physical device, use your computer's IP:
# http://192.168.1.100:8000

# Test connection
curl http://10.0.2.2:8000/health
```

### QR Scanning Not Working
1. Check camera permissions granted
2. Verify QR code format is correct
3. Check Gate Scanner backend URL
4. Verify scanner is authenticated
5. Check backend logs for validation errors

### Location Not Updating
1. Check location permissions granted
2. Verify GPS is enabled on device
3. Check Student App is in foreground
4. Verify network connectivity
5. Check backend receives POST requests

---

## Performance Testing

### Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test health endpoint
ab -n 1000 -c 10 http://localhost:8000/health

# Test authentication
ab -n 100 -c 5 -p login.json -T application/x-www-form-urlencoded http://localhost:8000/api/v1/auth/login
```

### Stress Testing Locations
```bash
# Simulate multiple students posting location
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/v1/location \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"student_id\": $i, \"latitude\": -1.23, \"longitude\": 36.78, \"accuracy\": 10, \"timestamp\": \"$(date -Iseconds)\"}" &
done
```

---

## Success Criteria

✅ All components start successfully  
✅ Full attendance flow works end-to-end  
✅ Location tracking works continuously  
✅ Notifications delivered to all parties  
✅ QR scanning validates and records  
✅ Reports generate accurate data  
✅ Real-time updates work (WebSocket)  
✅ Emergency alerts work immediately  
✅ All mobile apps authenticate  
✅ Admin portal displays all data  

---

## Conclusion

This testing guide covers all critical paths in the eSalama system. Follow each scenario systematically to ensure complete end-to-end functionality.

**All systems operational = Production Ready! 🎉**

---

*eSalama Schools - Securing every child's journey from home to school and back.*
