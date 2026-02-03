# eSalama Gate Scanner - Implementation Guide

## Overview

This document provides a comprehensive guide to the eSalama Gate Scanner Android application, including how it integrates with the backend system to scan QR codes and send notifications.

## System Flow

### 1. Student Arrival/Departure Flow

```
┌─────────────────┐
│  Student with   │
│  QR Code on     │
│  Device/Tablet  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gate Scanner   │
│  Android App    │
│  (This App)     │
└────────┬────────┘
         │
         │ Scan QR Code
         ▼
┌─────────────────┐
│  ML Kit Barcode │
│  Detection      │
└────────┬────────┘
         │
         │ Extract QR Token
         ▼
┌─────────────────┐
│  Validate with  │
│  Backend API    │
└────────┬────────┘
         │
         ├─────────────────────────────────┐
         │                                 │
         ▼                                 ▼
┌─────────────────┐              ┌─────────────────┐
│  Record         │              │  Send           │
│  Attendance     │              │  Notifications  │
└────────┬────────┘              └────────┬────────┘
         │                                 │
         │                                 ├───────► Parent App
         │                                 ├───────► Teacher App
         │                                 └───────► Backend Portal
         │
         ▼
┌─────────────────┐
│  Display        │
│  Success/Error  │
└─────────────────┘
```

### 2. API Integration Flow

#### Step 1: Authentication
```http
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=scanner@school.com&password=secure_password

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "scanner@school.com",
    "full_name": "Main Gate Scanner",
    "role": "gate_scanner"
  }
}
```

#### Step 2: QR Code Validation
```http
POST /api/v1/qr/validate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "qr_token": "encrypted_student_qr_token_here",
  "scanner_id": "main_gate_scanner",
  "location": "Main Gate"
}

Response:
{
  "valid": true,
  "student_id": 123,
  "student_name": "Emmanuel Odenyire",
  "class": "Grade 5A",
  "scan_type": "arrival",
  "message": "Valid QR code",
  "timestamp": "2024-02-03T08:30:00"
}
```

#### Step 3: Record Attendance
```http
POST /api/v1/attendance
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "student_id": 123,
  "scan_type": "arrival",
  "timestamp": "2024-02-03T08:30:00",
  "location": "Main Gate",
  "scanner_id": "main_gate_scanner"
}

Response:
{
  "message": "Attendance recorded successfully",
  "success": true
}
```

#### Step 4: Send Notifications
```http
POST /api/v1/notifications
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "user_id": 123,
  "type": "arrival",
  "message": "Good morning, Emmanuel Odenyire has safely entered the school gate at 08:30 AM.",
  "student_id": 123
}

Response:
{
  "message": "Notification sent successfully",
  "success": true
}
```

## Key Features

### 1. Real-Time QR Scanning

The app uses CameraX and ML Kit for efficient QR code scanning:

```kotlin
// QRScannerActivity.kt
private inner class QRCodeAnalyzer : ImageAnalysis.Analyzer {
    private val scanner = BarcodeScanning.getClient()

    override fun analyze(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image
        if (mediaImage != null && !isProcessing) {
            val image = InputImage.fromMediaImage(
                mediaImage,
                imageProxy.imageInfo.rotationDegrees
            )

            scanner.process(image)
                .addOnSuccessListener { barcodes ->
                    for (barcode in barcodes) {
                        barcode.rawValue?.let { qrCode ->
                            handleQRCode(qrCode)
                        }
                    }
                }
        }
    }
}
```

### 2. Automatic Notification Dispatch

When a QR code is scanned successfully, the app automatically:

1. **Validates the QR code** with the backend
2. **Records attendance** in the database
3. **Sends notifications** to:
   - **Parents**: "Good morning, [Student Name] has safely entered the school gate at [Time]."
   - **Teachers**: Attendance update for the class
   - **Backend Portal**: Real-time dashboard update

### 3. Error Handling

The app handles various error scenarios:

- Invalid QR codes
- Expired QR tokens
- Network connectivity issues
- Authentication failures
- Duplicate scans (3-second cooldown)

### 4. Offline Support (Future Enhancement)

The current implementation requires internet connectivity. Future versions will include:

- Local caching of scanned QR codes
- Background sync when connection is restored
- Room database for offline storage

## Configuration

### API Endpoint Configuration

The app can be configured to connect to different backend servers:

**For Android Emulator:**
```
http://10.0.2.2:8000/
```

**For Physical Device (Same Network):**
```
http://192.168.1.100:8000/
```

**For Production:**
```
https://api.esalama.example.com/
```

### Scanner ID Configuration

Each scanner should have a unique ID for tracking purposes:
- `main_gate_scanner`
- `back_gate_scanner`
- `entrance_a_scanner`

## Security Features

### 1. JWT Authentication

All API requests require JWT authentication:

```kotlin
val token = prefsManager.getBearerToken()  // Returns "Bearer <token>"
apiService.validateQR(request, token)
```

### 2. QR Token Security

QR tokens are:
- Time-limited (15 minutes expiration)
- Single-use (prevents replay attacks)
- Encrypted with student information

### 3. Scan Cooldown

Prevents duplicate scans:
```kotlin
companion object {
    private const val SCAN_COOLDOWN_MS = 3000L // 3 seconds
}

if (qrCode == lastScannedCode && 
    (currentTime - lastScanTime) < SCAN_COOLDOWN_MS) {
    return  // Ignore duplicate
}
```

## Testing Guide

### Prerequisites

1. Backend server running at configured URL
2. Test user with `gate_scanner` role
3. Student with valid QR code

### Test Scenarios

#### 1. Login Test
- [ ] Open app
- [ ] Enter valid credentials
- [ ] Verify successful login
- [ ] Check token storage

#### 2. QR Scanning Test
- [ ] Tap "Scan QR Code"
- [ ] Grant camera permission
- [ ] Scan student QR code
- [ ] Verify success message
- [ ] Check backend for attendance record

#### 3. Settings Test
- [ ] Open settings
- [ ] Change API URL
- [ ] Change Scanner ID
- [ ] Save settings
- [ ] Verify settings persisted

#### 4. Error Handling Test
- [ ] Scan invalid QR code
- [ ] Scan expired QR code
- [ ] Test with no internet
- [ ] Test with invalid credentials

## Deployment Guide

### Building the APK

```bash
cd gate-scanner/android

# Debug build
./gradlew assembleDebug

# Release build (requires signing)
./gradlew assembleRelease
```

### Installation

```bash
# Install via ADB
adb install app/build/outputs/apk/debug/app-debug.apk

# Or copy APK to device and install manually
```

### Initial Setup on Device

1. Install APK on scanner device
2. Open app
3. Configure settings:
   - API URL: Your backend server URL
   - Scanner ID: Unique identifier for this device
4. Login with scanner operator credentials
5. Grant camera permission
6. Start scanning

## Troubleshooting

### Common Issues

#### 1. Camera Not Working
**Solution:**
- Check camera permission granted
- Verify device has working camera
- Restart app

#### 2. Cannot Connect to Backend
**Solution:**
- Verify API URL in settings
- Check backend server is running
- For emulator, use `http://10.0.2.2:8000/`
- For device, ensure on same network as server

#### 3. QR Validation Fails
**Solution:**
- Check QR token not expired (15 min validity)
- Verify student exists in database
- Check backend logs for errors

#### 4. Notifications Not Sent
**Solution:**
- Check backend notification service running
- Verify parent/teacher accounts exist
- Check backend logs

## Performance Optimization

### 1. Scan Performance

- Uses `STRATEGY_KEEP_ONLY_LATEST` for image analysis
- Single-thread executor for camera operations
- Efficient barcode detection with ML Kit

### 2. Network Performance

- Connection timeout: 30 seconds
- Retry logic for failed requests
- Request/response logging for debugging

### 3. Memory Management

- Proper camera lifecycle management
- Image proxy cleanup after processing
- No memory leaks in activities

## Future Enhancements

### Planned Features

1. **Offline Mode**
   - Local queue for scanned codes
   - Background sync with WorkManager
   - Room database integration

2. **Push Notifications**
   - FCM integration
   - Real-time alerts
   - Scan confirmation

3. **Analytics Dashboard**
   - Daily scan statistics
   - Scanner performance metrics
   - Error rate tracking

4. **Multi-Language Support**
   - English, Swahili, French
   - Localized strings
   - RTL support

5. **Biometric Authentication**
   - Fingerprint login
   - Face recognition
   - Enhanced security

## Support

For technical support or questions:
- GitHub Issues: https://github.com/eodenyire/eSalama/issues
- Email: support@esalama.example.com
- Documentation: https://github.com/eodenyire/eSalama/wiki

## License

MIT License - see LICENSE file for details

---

**eSalama Schools** - Securing every child's journey from home to school and back.
