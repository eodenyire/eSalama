# eSalama Parent App

✅ **Status**: Complete and Production-Ready

A React Native mobile application for parents to receive real-time notifications and track their children's location during school commutes.

## Features

### ✅ Core Features (All Implemented)

- **🔔 Real-time Notifications Dashboard**
  - Receive instant alerts for student arrival/departure
  - Mark notifications as read
  - Pull-to-refresh for latest updates
  - Visual indicators for unread messages
  - Timestamp and notification type display

- **📍 Live GPS Tracking**
  - View child's current location on interactive map
  - Location history trail visualization (polyline)
  - Auto-refresh every 30 seconds
  - Manual refresh button
  - Accuracy and timestamp information
  - Custom markers for student locations

- **👤 Profile Management**
  - View account information (name, email, phone)
  - Secure logout with confirmation
  - Session management

- **🔐 Secure Authentication**
  - JWT-based login
  - Secure token storage with AsyncStorage
  - Automatic session persistence
  - Proper logout with cleanup

## Technical Stack

- **Framework**: React Native 0.73
- **Navigation**: React Navigation 6 (Stack & Bottom Tabs)
- **Maps**: React Native Maps 1.10.0
- **HTTP Client**: Axios 1.6.5
- **Storage**: AsyncStorage 1.21.0
- **Authentication**: JWT Bearer tokens

## Installation

### Prerequisites
- Node.js 16+ and npm
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)
- Backend API running (see `/backend` folder)

### Setup

1. **Install Dependencies**
   ```bash
   cd mobile/parent-app
   npm install
   ```

2. **Configure API Endpoint**
   
   Edit `src/config/api.js` to point to your backend:
   ```javascript
   export const API_BASE_URL = 'http://YOUR_BACKEND_URL:8000';
   // For Android emulator: http://10.0.2.2:8000
   // For iOS simulator: http://localhost:8000
   // For physical device: http://YOUR_COMPUTER_IP:8000
   ```

3. **Run on Android**
   ```bash
   npm run android
   ```

4. **Run on iOS**
   ```bash
   cd ios && pod install && cd ..
   npm run ios
   ```

## Project Structure

```
parent-app/
├── App.js                          # Main app with navigation
├── index.js                        # Entry point
├── package.json                    # Dependencies
├── src/
│   ├── config/
│   │   └── api.js                  # API endpoints configuration
│   ├── services/
│   │   └── auth.service.js         # Authentication service
│   └── screens/
│       ├── LoginScreen.js          # Login UI
│       ├── HomeScreen.js           # Notifications dashboard
│       ├── TrackingScreen.js       # GPS tracking map
│       └── ProfileScreen.js        # User profile & settings
```

## Usage

### Login
1. Launch the app
2. Enter parent email and password
3. Tap "Login"
4. Redirected to main app with bottom tabs

### View Notifications
1. Open app (default screen is Notifications)
2. Pull down to refresh
3. Tap notification to mark as read
4. Unread notifications show blue border and dot

### Track Child Location
1. Tap "Track" tab at bottom
2. View child's current location on map
3. Blue line shows location history trail
4. Location auto-refreshes every 30 seconds
5. Tap "Refresh Location" for manual update

### Manage Profile
1. Tap "Profile" tab at bottom
2. View account details
3. Tap "Logout" to sign out
4. Confirm logout in dialog

## API Integration

The app connects to the following backend endpoints:

### Authentication
- `POST /api/v1/auth/login` - Login with email/password
- `GET /api/v1/auth/me` - Get current user info

### Students
- `GET /api/v1/students` - Get list of children

### Location
- `GET /api/v1/location/{student_id}/last` - Get last known location
- `GET /api/v1/location/{student_id}/history` - Get location history

### Notifications
- `GET /api/v1/notifications` - Get all notifications
- `PUT /api/v1/notifications/{id}/read` - Mark notification as read

## Configuration

### Development vs Production

**Development** (localhost):
```javascript
export const API_BASE_URL = 'http://localhost:8000';
export const WS_BASE_URL = 'ws://localhost:8000';
```

**Production** (HTTPS):
```javascript
export const API_BASE_URL = 'https://api.esalama.com';
export const WS_BASE_URL = 'wss://api.esalama.com';
```

## Testing

### Manual Testing Checklist

- [x] Login with valid credentials
- [x] View notifications list
- [x] Pull-to-refresh notifications
- [x] Mark notification as read
- [x] View child location on map
- [x] Location history displays correctly
- [x] Auto-refresh works (30s)
- [x] Manual refresh button works
- [x] View profile information
- [x] Logout with confirmation
- [x] Token persists across app restarts

## Troubleshooting

### Common Issues

**Cannot connect to backend:**
- Verify backend is running
- Check API_BASE_URL in `src/config/api.js`
- For Android emulator, use `10.0.2.2` instead of `localhost`
- For physical device, ensure device and computer are on same network

**Map not displaying:**
- Check Google Maps API key (if required)
- Verify react-native-maps is installed
- Ensure location permissions granted

**Notifications not showing:**
- Check backend is running
- Verify authentication token is valid
- Check network connectivity
- Pull down to refresh notifications

**App crashes on startup:**
- Run `npm install` to ensure dependencies installed
- Clear Metro bundler cache: `npm start -- --reset-cache`
- Rebuild app: `npm run android` or `npm run ios`

## Security

- ✅ JWT token authentication
- ✅ Secure token storage (AsyncStorage)
- ✅ Authorization headers on all API calls
- ✅ HTTPS ready for production
- ✅ Proper session cleanup on logout

## Production Deployment

### Before Deployment
1. Update `API_BASE_URL` to production HTTPS endpoint
2. Configure app icons and splash screens
3. Set up signing certificates
4. Enable ProGuard/R8 obfuscation (Android)
5. Test on physical devices
6. Generate release builds

### Build Release

**Android:**
```bash
cd android
./gradlew assembleRelease
```

**iOS:**
```bash
cd ios
xcodebuild -workspace eSalamaParent.xcworkspace -scheme eSalamaParent archive
```

## Future Enhancements

Optional features for future iterations:

- [ ] Push notifications (Firebase Cloud Messaging)
- [ ] WebSocket real-time updates (currently using polling)
- [ ] Offline mode with data synchronization
- [ ] Multi-language support (i18n)
- [ ] Dark mode theme
- [ ] Biometric authentication (Face ID, Touch ID)
- [ ] In-app chat with teachers
- [ ] Export reports to PDF
- [ ] Video streaming (if required)

## Support

For issues or questions:
- Check backend is running: `http://localhost:8000/health`
- Review API documentation: `http://localhost:8000/docs`
- Verify network connectivity
- Check React Native logs: `npm start` and view Metro bundler output
- Review permissions in device settings

## License

MIT License - See LICENSE file in root directory

---

**eSalama Parent App** - Part of the eSalama Schools secure student tracking system.

**Status**: ✅ Complete and Production-Ready  
**Version**: 1.0.0  
**Last Updated**: February 4, 2026
