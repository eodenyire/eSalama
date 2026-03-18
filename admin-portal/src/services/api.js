import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  getCurrentUser: () => api.get('/auth/me'),
}

// Students API
export const studentsAPI = {
  getAll: (params) => api.get('/students', { params }),
  getOne: (id) => api.get(`/students/${id}`),
  create: (data) => api.post('/students', data),
  update: (id, data) => api.put(`/students/${id}`, data),
  updateDevice: (id, data) => api.put(`/students/${id}/device`, data),
}

// Attendance API
export const attendanceAPI = {
  record: (data) => api.post('/attendance', data),
  getRecords: (params) => api.get('/attendance', { params }),
}

// Location API
export const locationAPI = {
  post: (data) => api.post('/location', data),
  getLastLocation: (studentId) => api.get(`/location/${studentId}/last`),
  getHistory: (studentId, params) => api.get(`/location/${studentId}/history`, { params }),
}

// QR Code API
export const qrAPI = {
  generate: (data) => api.post('/qr/generate', data),
  validate: (data) => api.post('/qr/validate', data),
}

// Notifications API
export const notificationsAPI = {
  send: (data) => api.post('/notifications', data),
  getAll: (params) => api.get('/notifications', { params }),
  markAsRead: (id) => api.put(`/notifications/${id}/read`),
}

export default api
