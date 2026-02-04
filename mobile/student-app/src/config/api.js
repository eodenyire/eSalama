/**
 * API Configuration for eSalama Student App
 */

// Default API URL - can be changed in settings
export const API_BASE_URL = 'http://localhost:8000';
export const API_VERSION = 'v1';
export const API_PREFIX = `/api/${API_VERSION}`;

// API Endpoints
export const ENDPOINTS = {
  // Authentication
  LOGIN: `${API_PREFIX}/auth/login`,
  REGISTER: `${API_PREFIX}/auth/register`,
  ME: `${API_PREFIX}/auth/me`,
  
  // Students
  STUDENTS: `${API_PREFIX}/students`,
  STUDENT_DETAIL: (id) => `${API_PREFIX}/students/${id}`,
  STUDENT_DEVICE: (id) => `${API_PREFIX}/students/${id}/device`,
  
  // QR Code
  QR_GENERATE: `${API_PREFIX}/qr/generate`,
  QR_VALIDATE: `${API_PREFIX}/qr/validate`,
  
  // Location Tracking
  LOCATION: `${API_PREFIX}/location`,
  LOCATION_LAST: (studentId) => `${API_PREFIX}/location/${studentId}/last`,
  LOCATION_HISTORY: (studentId) => `${API_PREFIX}/location/${studentId}/history`,
  
  // Notifications
  NOTIFICATIONS: `${API_PREFIX}/notifications`,
  NOTIFICATION_READ: (id) => `${API_PREFIX}/notifications/${id}/read`,
};

// App Configuration
export const CONFIG = {
  // Location tracking interval (2 minutes in milliseconds)
  LOCATION_INTERVAL: 2 * 60 * 1000,
  
  // QR code refresh interval (every minute to ensure fresh token)
  QR_REFRESH_INTERVAL: 60 * 1000,
  
  // QR token expiration (15 minutes)
  QR_TOKEN_EXPIRY: 15 * 60 * 1000,
  
  // GPS accuracy threshold (meters)
  GPS_ACCURACY_THRESHOLD: 50,
};

export default {
  API_BASE_URL,
  API_PREFIX,
  ENDPOINTS,
  CONFIG,
};
