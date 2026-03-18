package com.esalama.gatescanner.data.api

import com.esalama.gatescanner.data.model.*
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit API interface for eSalama backend
 */
interface ESalamaApiService {

    @POST("api/v1/auth/login")
    @FormUrlEncoded
    suspend fun login(
        @Field("username") username: String,
        @Field("password") password: String
    ): Response<LoginResponse>

    @POST("api/v1/qr/validate")
    suspend fun validateQR(
        @Body request: QRValidationRequest,
        @Header("Authorization") token: String
    ): Response<QRValidationResponse>

    @POST("api/v1/attendance")
    suspend fun recordAttendance(
        @Body record: AttendanceRecord,
        @Header("Authorization") token: String
    ): Response<ApiResponse>

    @POST("api/v1/notifications")
    suspend fun sendNotification(
        @Body notification: NotificationRequest,
        @Header("Authorization") token: String
    ): Response<ApiResponse>

    @GET("api/v1/auth/me")
    suspend fun getCurrentUser(
        @Header("Authorization") token: String
    ): Response<User>
}
