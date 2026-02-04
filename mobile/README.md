# eSalama Mobile Applications

Three React Native mobile applications for the eSalama Schools secure student tracking system.

## Applications

### 1. Student App (`/student-app`)
Mobile application for students to:
- Generate auto-refreshing QR codes for attendance
- Enable GPS location tracking (every 2 minutes)
- Send emergency SOS alerts
- View tracking status

**Key Features:**
- Auto-refreshing QR codes (refresh every minute, expire after 15 minutes)
- Automatic GPS location posting to backend
- Emergency SOS button with instant notification
- Real-time status monitoring

### 2. Parent App (`/parent-app`)
Mobile application for parents to:
- Receive real-time arrival/departure notifications
- Track child's location on live map
- View location history trail
- Manage account settings

**Key Features:**
- Push notifications for student arrival/departure
- Live GPS tracking with map view
- Location history visualization
- Attendance history

### 3. Teacher App (`/teacher-app`)
Mobile application for teachers to:
- Monitor class attendance in real-time
- View student arrival/departure times
- Send notifications to parents
- Track notification history

**Key Features:**
- Real-time class attendance monitoring
- Send custom notifications to parents
- View student details
- Attendance reports by date

## Technical Stack

All three apps are built with:
- **Framework**: React Native 0.73
- **Navigation**: React Navigation 6 (Stack & Bottom Tabs)
- **Storage**: AsyncStorage for token persistence
- **HTTP Client**: Axios for API communication
- **Authentication**: JWT-based with secure token storage

### Additional Libraries

**Student App:**
- react-native-qrcode-svg - QR code generation
- react-native-geolocation-service - GPS tracking
- react-native-permissions - Permission management

**Parent App:**
- react-native-maps - Map visualization
- WebSocket support for real-time updates

## Installation

### Prerequisites
- Node.js 16+
- React Native development environment
- Android Studio (for Android) or Xcode (for iOS)
- Backend API running (see `/backend` folder)

### Setup Each App

1. **Install Dependencies**
   ```bash
   cd student-app  # or parent-app or teacher-app
   npm install
   ```

2. **Configure API Endpoint**
   Edit `src/config/api.js` in each app:
   ```javascript
   export const API_BASE_URL = 'http://YOUR_BACKEND_URL:8000';
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

## API Integration

All apps connect to the eSalama backend API:

### Authentication
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user info

### Student App APIs
- `POST /api/v1/qr/generate` - Generate QR code
- `POST /api/v1/location` - Post GPS coordinates
- `POST /api/v1/notifications` - Send SOS alert

### Parent App APIs
- `GET /api/v1/students` - Get children list
- `GET /api/v1/location/{student_id}/last` - Get last location
- `GET /api/v1/location/{student_id}/history` - Get location history
- `GET /api/v1/notifications` - Get notifications
- `WS /api/v1/streaming/location/{student_id}` - Real-time location updates

### Teacher App APIs
- `GET /api/v1/students` - Get student list
- `GET /api/v1/attendance` - Get attendance records
- `POST /api/v1/notifications` - Send notification to parent
- `GET /api/v1/reports/attendance` - Get attendance report

## End-to-End Workflow

### 1. Student Attendance Flow
1. **Student** opens Student App and logs in
2. App automatically starts GPS tracking
3. App generates and displays QR code
4. **Gate Scanner** scans QR code at school gate
5. Backend validates QR and records attendance
6. **Parent** receives instant notification
7. **Teacher** sees updated class attendance
8. **Admin Portal** dashboard updates in real-time

### 2. Location Tracking Flow
1. **Student App** posts GPS location every 2 minutes
2. Backend stores location in database
3. **Parent App** fetches and displays location on map
4. Location history shows trail of student's journey
5. Real-time updates via WebSocket (optional)

### 3. Communication Flow
1. **Teacher** selects student and writes message
2. Teacher App sends notification via backend
3. Backend routes notification to parent's account
4. **Parent** receives notification in Parent App
5. Notification stored in database with read status

### 4. Emergency Flow
1. **Student** presses SOS button
2. Student App sends emergency notification
3. Backend immediately notifies:
   - Parent (push notification + SMS)
   - Teacher (in-app notification)
   - Admin Portal (alert)
4. All parties can respond appropriately

## Development

### Project Structure
```
mobile/
├── student-app/
│   ├── src/
│   │   ├── config/           # API configuration
│   │   ├── services/         # Auth, Location, QR services
│   │   ├── screens/          # Login, Home screens
│   │   └── components/       # Reusable components
│   ├── App.js               # Main app component
│   └── package.json         # Dependencies
│
├── parent-app/
│   ├── src/
│   │   ├── config/           # API configuration
│   │   ├── services/         # Auth service
│   │   ├── screens/          # Login, Home, Tracking, Profile
│   │   └── components/       # Reusable components
│   ├── App.js               # Main app with tabs
│   └── package.json         # Dependencies
│
└── teacher-app/
    ├── src/
    │   ├── config/           # API configuration
    │   ├── services/         # Auth service
    │   ├── screens/          # Login, Attendance, Notifications, Profile
    │   └── components/       # Reusable components
    ├── App.js               # Main app with tabs
    └── package.json         # Dependencies
```

### Adding New Features

1. Create service in `src/services/` for API logic
2. Create screen in `src/screens/` for UI
3. Add route in `App.js` navigation
4. Update API config if new endpoints needed

## Testing

### Manual Testing

**Student App:**
- [ ] Login with student credentials
- [ ] QR code generates and refreshes
- [ ] GPS location posts every 2 minutes
- [ ] SOS alert sends successfully

**Parent App:**
- [ ] Login with parent credentials
- [ ] View list of children
- [ ] See child's location on map
- [ ] Receive notifications

**Teacher App:**
- [ ] Login with teacher credentials
- [ ] View class attendance
- [ ] Send notification to parent
- [ ] View notification history

### Integration Testing

1. Start backend server
2. Create test accounts (student, parent, teacher)
3. Test full attendance flow:
   - Student generates QR
   - Gate scanner scans QR
   - Parent receives notification
   - Teacher sees attendance update
4. Test location tracking:
   - Student app posts location
   - Parent app displays location
5. Test notifications:
   - Teacher sends message
   - Parent receives notification

## Troubleshooting

### Common Issues

**QR Code Not Generating:**
- Check backend is running
- Verify API endpoint URL
- Check authentication token

**Location Not Updating:**
- Ensure location permissions granted
- Check GPS is enabled
- Verify network connectivity

**Notifications Not Showing:**
- Check notification permissions
- Verify backend is sending notifications
- Check WebSocket connection (if using)

**App Crashes:**
- Clear app data and reinstall
- Check React Native environment
- Review console logs

## Security

- JWT tokens stored securely in AsyncStorage
- All API calls use HTTPS in production
- QR codes time-limited (15 minutes)
- Location data encrypted in transit
- Permissions properly requested

## Production Deployment

### Before Deploying

1. Update API endpoints to production URLs
2. Enable HTTPS for all API calls
3. Configure push notification services
4. Set up analytics and crash reporting
5. Test on multiple devices
6. Enable ProGuard/code obfuscation
7. Generate signed APK/IPA

### App Store Submission

1. Create app icons and screenshots
2. Write app descriptions
3. Configure app privacy policy
4. Submit to Google Play Store
5. Submit to Apple App Store

## Future Enhancements

- [ ] Push notifications (Firebase Cloud Messaging)
- [ ] Offline mode with data sync
- [ ] Multi-language support
- [ ] Dark mode
- [ ] Biometric authentication
- [ ] In-app chat
- [ ] Video streaming
- [ ] Attendance history graphs
- [ ] Export reports to PDF

## Support

For issues or questions:
- Check backend is running: `http://localhost:8000/health`
- Review API documentation: `http://localhost:8000/docs`
- Check React Native logs
- Verify network connectivity
- Review permissions in device settings

## License

MIT License - See LICENSE file in root directory

---

**eSalama Mobile Apps** - Part of the eSalama Schools secure student tracking system.
