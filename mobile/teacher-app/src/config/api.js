/**
 * API Configuration for eSalama Teacher App
 */

export const API_BASE_URL = 'http://localhost:8000';
export const API_VERSION = 'v1';
export const API_PREFIX = `/api/${API_VERSION}`;

export const ENDPOINTS = {
  LOGIN: `${API_PREFIX}/auth/login`,
  ME: `${API_PREFIX}/auth/me`,
  STUDENTS: `${API_PREFIX}/students`,
  ATTENDANCE: `${API_PREFIX}/attendance`,
  NOTIFICATIONS: `${API_PREFIX}/notifications`,
  NOTIFICATION_READ: (id) => `${API_PREFIX}/notifications/${id}/read`,
  REPORTS_ATTENDANCE: `${API_PREFIX}/reports/attendance`,
};

export default { API_BASE_URL, API_PREFIX, ENDPOINTS };
