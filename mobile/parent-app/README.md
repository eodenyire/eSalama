# eSalama Parent App

A React Native mobile application for parents to receive real-time notifications and track their children's location.

## Features

- **Real-time Notifications**: Receive instant alerts for arrival/departure
- **Live GPS Tracking**: View child's location on map with history trail
- **Attendance History**: View all attendance records
- **Profile Management**: View and manage account settings

## Technical Stack

- React Native 0.73
- React Navigation (Stack & Bottom Tabs)
- React Native Maps
- Axios for API communication
- AsyncStorage for token persistence

## Installation

```bash
cd mobile/parent-app
npm install
```

Configure API endpoint in `src/config/api.js` and run with `npm run android` or `npm run ios`.

## License

MIT License
