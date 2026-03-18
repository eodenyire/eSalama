# eSalama Gate Scanner - Android Application

## Overview

The eSalama Gate Scanner is an Android application designed to scan student QR codes at school gates and automatically:
- Validate the QR code with the backend server
- Record attendance (arrival/departure)
- Send notifications to parents
- Send notifications to teachers
- Update the backend portal

## Features

✅ **QR Code Scanning**
- Real-time QR code detection using ML Kit
- Camera integration with CameraX
- Automatic barcode recognition

✅ **Backend Integration**
- RESTful API communication with eSalama backend
- JWT-based authentication
- Real-time attendance recording
- Automatic notification dispatch

✅ **Offline Support**
- Configurable API endpoint
- Network status handling
- Error recovery

✅ **User Authentication**
- Secure login for scanner operators
- JWT token management
- Session persistence

✅ **Settings Management**
- Configurable API base URL
- Scanner device ID configuration
- Easy setup for multiple scanners

## Technology Stack

- **Language**: Kotlin
- **UI**: Material Design Components
- **Camera**: CameraX
- **QR Scanning**: ML Kit Barcode Scanning
- **Networking**: Retrofit + OkHttp
- **JSON**: Gson
- **Async**: Kotlin Coroutines
- **Architecture**: MVVM-ready structure

## Requirements

- Android 7.0 (API 24) or higher
- Camera permission
- Internet connection
- eSalama backend server running

## Setup Instructions

### 1. Prerequisites

- Android Studio Hedgehog (2023.1.1) or later
- JDK 8 or higher
- Android SDK with API 34

### 2. Clone the Repository

```bash
git clone https://github.com/eodenyire/eSalama.git
cd eSalama/gate-scanner/android
```

### 3. Open in Android Studio

1. Open Android Studio
2. Select "Open an existing project"
3. Navigate to `eSalama/gate-scanner/android`
4. Wait for Gradle sync to complete

### 4. Build the Project

```bash
# From command line
./gradlew build

# Or use Android Studio:
# Build > Make Project
```

### 5. Run on Device/Emulator

1. Connect an Android device or start an emulator
2. Click "Run" in Android Studio or use:

```bash
./gradlew installDebug
```

## Configuration

### First-Time Setup

1. **Launch the app**
2. **Go to Settings** (before login)
3. **Configure API URL**:
   - For emulator: `http://10.0.2.2:8000/`
   - For physical device: `http://YOUR_SERVER_IP:8000/`
4. **Set Scanner ID**: e.g., `main_gate_scanner`
5. **Save settings**

### Login

Use credentials for a user with `gate_scanner` role:
- Username: scanner operator email
- Password: scanner operator password

### Scanning QR Codes

1. Tap "Scan QR Code" on main screen
2. Point camera at student's QR code
3. Wait for automatic validation
4. View success/error message
5. Notifications are sent automatically

## API Integration

The app integrates with the following eSalama backend endpoints:

### Authentication
- `POST /api/v1/auth/login` - Login with credentials

### QR Validation
- `POST /api/v1/qr/validate` - Validate scanned QR code

### Attendance
- `POST /api/v1/attendance` - Record attendance

### Notifications
- `POST /api/v1/notifications` - Send notifications to parents/teachers

## Architecture

```
app/
├── data/
│   ├── api/
│   │   ├── ESalamaApiService.kt      # Retrofit API interface
│   │   └── RetrofitClient.kt         # API client configuration
│   └── model/
│       └── Models.kt                  # Data models
├── ui/
│   ├── LoginActivity.kt               # Login screen
│   ├── QRScannerActivity.kt          # QR scanning screen
│   └── SettingsActivity.kt           # Settings screen
├── utils/
│   └── PreferencesManager.kt         # SharedPreferences wrapper
└── MainActivity.kt                    # Main dashboard
```

## Permissions

The app requires the following permissions:

- `CAMERA` - For QR code scanning
- `INTERNET` - For API communication
- `ACCESS_NETWORK_STATE` - To check connectivity

## Troubleshooting

### Camera not working
- Check that CAMERA permission is granted
- Ensure device has a working camera
- Try restarting the app

### Cannot connect to backend
- Verify API URL in Settings
- Check that backend server is running
- For emulator, use `http://10.0.2.2:8000/`
- For device, ensure device and server are on same network

### Login fails
- Verify credentials are correct
- Check user has appropriate role (gate_scanner)
- Verify backend is accessible

### QR validation fails
- Ensure QR code is from eSalama student app
- Check that QR token is not expired (15 min validity)
- Verify student exists in database

## Testing

### Unit Tests
```bash
./gradlew test
```

### Instrumentation Tests
```bash
./gradlew connectedAndroidTest
```

## Building APK

### Debug APK
```bash
./gradlew assembleDebug
# Output: app/build/outputs/apk/debug/app-debug.apk
```

### Release APK
```bash
./gradlew assembleRelease
# Output: app/build/outputs/apk/release/app-release.apk
```

## Security Features

- JWT token-based authentication
- Secure HTTPS communication (when configured)
- Token storage in encrypted SharedPreferences
- 3-second scan cooldown to prevent duplicates
- Input validation

## Future Enhancements

- [ ] Offline queue for failed scans
- [ ] Local database with Room
- [ ] WorkManager for background sync
- [ ] Push notifications
- [ ] Scan history
- [ ] Multiple language support
- [ ] Dark theme support
- [ ] Biometric authentication

## Support

For issues or questions:
- GitHub Issues: https://github.com/eodenyire/eSalama/issues
- Email: support@esalama.example.com

## License

MIT License - see LICENSE file for details

## Contributors

- eSalama Development Team

---

**eSalama Schools** - Securing every child's journey from home to school and back.
