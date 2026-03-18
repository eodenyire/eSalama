/**
 * QR Code Service
 * Generates and manages QR codes for attendance
 */
import AuthService from './auth.service';
import { ENDPOINTS } from '../config/api';

class QRService {
  constructor() {
    this.currentQRCode = null;
    this.currentToken = null;
    this.expiresAt = null;
  }

  /**
   * Generate QR code for attendance
   */
  async generateQRCode(studentId, attendanceType = 'arrival') {
    try {
      const api = AuthService.getAxiosInstance();
      const response = await api.post(ENDPOINTS.QR_GENERATE, {
        student_id: studentId,
        attendance_type: attendanceType,
      });

      const { qr_code, token, expires_at } = response.data;
      
      this.currentQRCode = qr_code;
      this.currentToken = token;
      this.expiresAt = new Date(expires_at);

      console.log('QR Code generated:', { token, expires_at });
      
      return {
        qrCode: qr_code,
        token,
        expiresAt: this.expiresAt,
      };
    } catch (error) {
      console.error('Error generating QR code:', error);
      throw error;
    }
  }

  /**
   * Check if current QR code is expired
   */
  isExpired() {
    if (!this.expiresAt) return true;
    return new Date() >= this.expiresAt;
  }

  /**
   * Get current QR code data
   */
  getCurrentQRCode() {
    return {
      qrCode: this.currentQRCode,
      token: this.currentToken,
      expiresAt: this.expiresAt,
      isExpired: this.isExpired(),
    };
  }

  /**
   * Clear current QR code
   */
  clear() {
    this.currentQRCode = null;
    this.currentToken = null;
    this.expiresAt = null;
  }
}

export default new QRService();
