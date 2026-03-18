# eSalama Gate Scanner

## Overview

The eSalama Gate Scanner is responsible for scanning student QR codes at school gates and automatically recording attendance while sending notifications to parents, teachers, and the backend portal.

## Components

### Android Application

A complete Android application for QR code scanning with the following features:

- **QR Code Scanning**: Real-time QR code detection using ML Kit and CameraX
- **Backend Integration**: RESTful API communication with JWT authentication
- **Attendance Recording**: Automatic attendance recording on scan
- **Notification System**: Sends alerts to parents, teachers, and backend portal
- **Offline Support**: Configurable for various network environments
- **User Authentication**: Secure login for scanner operators

**Location**: `/android/`

See [Android README](android/README.md) for detailed setup instructions.

### Hardware Scanner (Future)

Planned hardware implementation for dedicated scanning devices.

## Quick Start

### Android Application

1. Open the project in Android Studio:
   ```bash
   cd android
   # Open in Android Studio
   ```

2. Build and run:
   ```bash
   ./gradlew installDebug
   ```

3. Configure the app:
   - Set API URL (e.g., `http://10.0.2.2:8000/` for emulator)
   - Set Scanner ID (e.g., `main_gate_scanner`)
   - Login with scanner operator credentials

4. Start scanning:
   - Tap "Scan QR Code"
   - Point camera at student QR code
   - Automatic validation and notification

## Technology Stack

- **Android**: Kotlin, CameraX, ML Kit
- **Networking**: Retrofit, OkHttp
- **Architecture**: MVVM-ready structure
- **UI**: Material Design Components

## Integration with Backend

The scanner integrates with the following eSalama backend endpoints:

- `POST /api/v1/auth/login` - Authentication
- `POST /api/v1/qr/validate` - QR code validation
- `POST /api/v1/attendance` - Attendance recording
- `POST /api/v1/notifications` - Notification dispatch

## Features

✅ Real-time QR code scanning
✅ Automatic attendance recording
✅ Multi-party notifications (parents, teachers, portal)
✅ Configurable API endpoint
✅ Secure authentication
✅ Error handling and validation
✅ Material Design UI

## Directory Structure

```
gate-scanner/
├── android/              # Android application
│   ├── app/
│   │   └── src/
│   │       └── main/
│   │           ├── java/com/esalama/gatescanner/
│   │           │   ├── data/        # Data layer (API, models)
│   │           │   ├── ui/          # UI layer (Activities)
│   │           │   └── utils/       # Utilities
│   │           └── res/             # Resources (layouts, strings, etc.)
│   ├── build.gradle
│   └── README.md
├── config/              # Configuration files
├── offline-cache/       # Offline caching (future)
└── src/                 # Additional scanner implementations
    ├── camera/          # Camera integration
    ├── qr-scanner/      # QR scanning logic
    ├── sync/            # Sync mechanisms
    └── validation/      # Validation logic
```

## Contributing

See main repository [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](../LICENSE) file for details.

---

**eSalama Schools** - Securing every child's journey from home to school and back.
