package com.esalama.gatescanner.data.model

import com.google.gson.annotations.SerializedName

/**
 * Data models for API communication
 */

data class LoginRequest(
    @SerializedName("username")
    val username: String,
    @SerializedName("password")
    val password: String
)

data class LoginResponse(
    @SerializedName("access_token")
    val accessToken: String,
    @SerializedName("token_type")
    val tokenType: String,
    @SerializedName("user")
    val user: User
)

data class User(
    @SerializedName("id")
    val id: Int,
    @SerializedName("email")
    val email: String,
    @SerializedName("full_name")
    val fullName: String,
    @SerializedName("role")
    val role: String
)

data class QRValidationRequest(
    @SerializedName("qr_token")
    val qrToken: String,
    @SerializedName("scanner_id")
    val scannerId: String? = null,
    @SerializedName("location")
    val location: String? = null
)

data class QRValidationResponse(
    @SerializedName("valid")
    val valid: Boolean,
    @SerializedName("student_id")
    val studentId: Int? = null,
    @SerializedName("student_name")
    val studentName: String? = null,
    @SerializedName("class")
    val studentClass: String? = null,
    @SerializedName("scan_type")
    val scanType: String? = null, // "arrival" or "departure"
    @SerializedName("message")
    val message: String? = null,
    @SerializedName("timestamp")
    val timestamp: String? = null
)

data class AttendanceRecord(
    @SerializedName("id")
    val id: Int? = null,
    @SerializedName("student_id")
    val studentId: Int,
    @SerializedName("scan_type")
    val scanType: String, // "arrival" or "departure"
    @SerializedName("timestamp")
    val timestamp: String,
    @SerializedName("location")
    val location: String? = null,
    @SerializedName("scanner_id")
    val scannerId: String? = null
)

data class NotificationRequest(
    @SerializedName("user_id")
    val userId: Int,
    @SerializedName("type")
    val type: String, // "arrival", "departure", "alert"
    @SerializedName("message")
    val message: String,
    @SerializedName("student_id")
    val studentId: Int? = null
)

data class ApiResponse(
    @SerializedName("message")
    val message: String,
    @SerializedName("success")
    val success: Boolean = true
)

data class ErrorResponse(
    @SerializedName("detail")
    val detail: String
)
