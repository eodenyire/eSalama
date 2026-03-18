# eSalama Admin Portal

React-based web frontend for the eSalama Schools administration portal.

## Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: TanStack Query (React Query)
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Maps**: React Leaflet (for location tracking)
- **Charts**: Recharts (for analytics)

## Features

- Modern, responsive admin dashboard
- User authentication and authorization
- Student management interface
- Real-time attendance monitoring
- GPS location tracking visualization
- QR code management
- Notification system
- Reports and analytics

## Setup Instructions

### Prerequisites

- Node.js 16 or higher
- npm or yarn package manager
- Backend API running (see backend README)

### Installation

1. **Navigate to admin-portal directory**:
   ```bash
   cd eSalama/admin-portal
   ```

2. **Install dependencies**:
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment**:
   
   The application expects the backend API to be available at `http://localhost:8000`. 
   This is configured in `vite.config.js` as a proxy.
   
   If your backend is running on a different URL, update the proxy configuration.

### Running the Application

**Development mode**:
```bash
npm run dev
# or
yarn dev
```

The application will be available at `http://localhost:3000`

**Production build**:
```bash
npm run build
# or
yarn build
```

**Preview production build**:
```bash
npm run preview
# or
yarn preview
```

## Project Structure

```
admin-portal/
├── public/              # Static assets
├── src/
│   ├── components/     # Reusable UI components
│   │   └── Layout.jsx  # Main layout with navigation
│   ├── contexts/       # React contexts
│   │   └── AuthContext.jsx  # Authentication context
│   ├── pages/          # Page components
│   │   ├── Login.jsx         # Login page
│   │   ├── Dashboard.jsx     # Main dashboard
│   │   ├── Students.jsx      # Student management
│   │   ├── Attendance.jsx    # Attendance tracking
│   │   └── MapView.jsx       # Location map view
│   ├── services/       # API services
│   │   └── api.js      # Axios configuration and API calls
│   ├── App.jsx         # Main app component
│   ├── main.jsx        # Entry point
│   └── index.css       # Global styles with Tailwind
├── index.html          # HTML template
├── vite.config.js      # Vite configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
└── package.json        # Dependencies and scripts
```

## Key Features

### Authentication
- JWT-based authentication
- Protected routes
- Automatic token refresh
- Role-based access control

### Dashboard
- Real-time statistics
- Student presence tracking
- Recent activity feed
- Alert notifications

### Student Management
- View all students
- Student details
- Device assignment
- Status management

### Attendance
- Daily attendance records
- Arrival/departure tracking
- Date-based filtering
- Location information

### Map View
- Real-time student locations
- Route visualization
- Geo-fencing display
- Historical tracking

## API Integration

The frontend communicates with the backend API through Axios. All API calls are defined in `src/services/api.js`.

Key API modules:
- `authAPI` - Authentication
- `studentsAPI` - Student management
- `attendanceAPI` - Attendance records
- `locationAPI` - GPS tracking
- `qrAPI` - QR code operations
- `notificationsAPI` - Notifications

## Default Login

For testing purposes, you'll need to create an admin user in the backend first:

```bash
# Use the backend API to register an admin user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "admin123",
    "full_name": "Admin User",
    "role": "admin"
  }'
```

## Development

### Code Style
- ESLint for code linting
- Tailwind CSS for styling
- Component-based architecture

### Adding New Pages
1. Create a new component in `src/pages/`
2. Add route in `src/App.jsx`
3. Add navigation link in `src/components/Layout.jsx`

## Docker

Build and run with Docker:

```bash
# Build image
docker build -t esalama-admin-portal .

# Run container
docker run -p 3000:3000 esalama-admin-portal
```

## Contributing

Please refer to the main repository's contributing guidelines.

## License

MIT License - see LICENSE file for details
