/**
 * Authentication Service - Parent App
 */
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_BASE_URL, ENDPOINTS } from '../config/api';

const TOKEN_KEY = 'esalama_parent_token';
const USER_KEY = 'esalama_parent_user';

class AuthService {
  constructor() {
    this.token = null;
    this.user = null;
  }

  async initialize() {
    try {
      this.token = await AsyncStorage.getItem(TOKEN_KEY);
      const userStr = await AsyncStorage.getItem(USER_KEY);
      if (userStr) {
        this.user = JSON.parse(userStr);
      }
    } catch (error) {
      console.error('Error loading auth data:', error);
    }
  }

  async login(email, password) {
    try {
      const response = await axios.post(`${API_BASE_URL}${ENDPOINTS.LOGIN}`, {
        username: email,
        password: password,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = response.data;
      this.token = access_token;
      
      await AsyncStorage.setItem(TOKEN_KEY, access_token);
      await this.fetchUserInfo();
      
      return { success: true, token: access_token };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: error.response?.data?.detail || 'Login failed' };
    }
  }

  async fetchUserInfo() {
    try {
      const response = await axios.get(`${API_BASE_URL}${ENDPOINTS.ME}`, {
        headers: { 'Authorization': `Bearer ${this.token}` },
      });
      this.user = response.data;
      await AsyncStorage.setItem(USER_KEY, JSON.stringify(response.data));
      return this.user;
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    }
  }

  async logout() {
    this.token = null;
    this.user = null;
    await AsyncStorage.removeItem(TOKEN_KEY);
    await AsyncStorage.removeItem(USER_KEY);
  }

  isAuthenticated() {
    return !!this.token;
  }

  getToken() {
    return this.token;
  }

  getUser() {
    return this.user;
  }

  getAxiosInstance() {
    return axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
    });
  }
}

export default new AuthService();
