# eSalama Student App

A React Native mobile application for students to generate QR codes for attendance tracking and enable GPS location monitoring.

## Features

### Core Functionality
- **Auto-refreshing QR Code Generation**: QR codes refresh every minute and expire after 15 minutes
- **GPS Location Tracking**: Automatically sends GPS coordinates to backend every 2 minutes
- **Emergency SOS Alerts**: One-tap emergency notification system
- **Real-time Status Monitoring**: Visual indicators for active tracking
- **Secure Authentication**: JWT-based authentication with token management

## Technical Stack

- **Framework**: React Native 0.73
- **Navigation**: React Navigation 6
- **Storage**: AsyncStorage for token persistence
- **HTTP Client**: Axios for API communication
- **QR Generation**: react-native-qrcode-svg
- **Location**: react-native-geolocation-service

## Installation

```bash
cd mobile/student-app
npm install
```

Configure API endpoint in `src/config/api.js` and run with `npm run android` or `npm run ios`.

## License

MIT License
