package com.esalama.gatescanner.utils

import android.content.Context
import android.content.SharedPreferences

/**
 * Preferences manager for storing app settings and auth token
 */
class PreferencesManager(context: Context) {
    
    private val prefs: SharedPreferences = context.getSharedPreferences(
        PREFS_NAME, Context.MODE_PRIVATE
    )

    companion object {
        private const val PREFS_NAME = "esalama_gate_scanner_prefs"
        private const val KEY_AUTH_TOKEN = "auth_token"
        private const val KEY_USER_EMAIL = "user_email"
        private const val KEY_USER_NAME = "user_name"
        private const val KEY_USER_ROLE = "user_role"
        private const val KEY_API_BASE_URL = "api_base_url"
        private const val KEY_SCANNER_ID = "scanner_id"
        private const val DEFAULT_API_URL = "http://10.0.2.2:8000/"
    }

    fun saveAuthToken(token: String) {
        prefs.edit().putString(KEY_AUTH_TOKEN, token).apply()
    }

    fun getAuthToken(): String? {
        return prefs.getString(KEY_AUTH_TOKEN, null)
    }

    fun saveUserInfo(email: String, name: String, role: String) {
        prefs.edit().apply {
            putString(KEY_USER_EMAIL, email)
            putString(KEY_USER_NAME, name)
            putString(KEY_USER_ROLE, role)
            apply()
        }
    }

    fun getUserEmail(): String? {
        return prefs.getString(KEY_USER_EMAIL, null)
    }

    fun getUserName(): String? {
        return prefs.getString(KEY_USER_NAME, null)
    }

    fun getUserRole(): String? {
        return prefs.getString(KEY_USER_ROLE, null)
    }

    fun setApiBaseUrl(url: String) {
        prefs.edit().putString(KEY_API_BASE_URL, url).apply()
    }

    fun getApiBaseUrl(): String {
        return prefs.getString(KEY_API_BASE_URL, DEFAULT_API_URL) ?: DEFAULT_API_URL
    }

    fun setScannerId(id: String) {
        prefs.edit().putString(KEY_SCANNER_ID, id).apply()
    }

    fun getScannerId(): String {
        return prefs.getString(KEY_SCANNER_ID, "scanner_001") ?: "scanner_001"
    }

    fun isLoggedIn(): Boolean {
        return getAuthToken() != null
    }

    fun clearAuth() {
        prefs.edit().apply {
            remove(KEY_AUTH_TOKEN)
            remove(KEY_USER_EMAIL)
            remove(KEY_USER_NAME)
            remove(KEY_USER_ROLE)
            apply()
        }
    }

    fun getBearerToken(): String? {
        return getAuthToken()?.let { "Bearer $it" }
    }
}
