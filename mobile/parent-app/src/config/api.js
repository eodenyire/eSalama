/**
 * API Configuration for eSalama Parent App
 */

export const API_BASE_URL = 'http://localhost:8000';
export const API_VERSION = 'v1';
export const API_PREFIX = `/api/${API_VERSION}`;

export const ENDPOINTS = {
  LOGIN: `${API_PREFIX}/auth/login`,
  ME: `${API_PREFIX}/auth/me`,
  STUDENTS: `${API_PREFIX}/students`,
  LOCATION_LAST: (studentId) => `${API_PREFIX}/location/${studentId}/last`,
  LOCATION_HISTORY: (studentId) => `${API_PREFIX}/location/${studentId}/history`,
  ATTENDANCE: `${API_PREFIX}/attendance`,
  NOTIFICATIONS: `${API_PREFIX}/notifications`,
  NOTIFICATION_READ: (id) => `${API_PREFIX}/notifications/${id}/read`,
};

export const WS_BASE_URL = 'ws://localhost:8000';
export const WS_ENDPOINTS = {
  LOCATION: (studentId, token) => `${WS_BASE_URL}${API_PREFIX}/streaming/location/${studentId}?token=${token}`,
  NOTIFICATIONS: (token) => `${WS_BASE_URL}${API_PREFIX}/streaming/notifications?token=${token}`,
};

export default { API_BASE_URL, API_PREFIX, ENDPOINTS, WS_BASE_URL, WS_ENDPOINTS };
