package com.esalama.gatescanner.ui

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.esalama.gatescanner.R
import com.esalama.gatescanner.data.api.RetrofitClient
import com.esalama.gatescanner.utils.PreferencesManager
import kotlinx.coroutines.launch

/**
 * Login activity for scanner operator authentication
 */
class LoginActivity : AppCompatActivity() {

    private lateinit var usernameEditText: EditText
    private lateinit var passwordEditText: EditText
    private lateinit var loginButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var prefsManager: PreferencesManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        prefsManager = PreferencesManager(this)

        // Initialize views
        usernameEditText = findViewById(R.id.usernameEditText)
        passwordEditText = findViewById(R.id.passwordEditText)
        loginButton = findViewById(R.id.loginButton)
        progressBar = findViewById(R.id.progressBar)

        loginButton.setOnClickListener {
            val username = usernameEditText.text.toString().trim()
            val password = passwordEditText.text.toString().trim()

            if (validateInput(username, password)) {
                performLogin(username, password)
            }
        }
    }

    private fun validateInput(username: String, password: String): Boolean {
        if (username.isEmpty()) {
            usernameEditText.error = "Username is required"
            return false
        }
        if (password.isEmpty()) {
            passwordEditText.error = "Password is required"
            return false
        }
        return true
    }

    private fun performLogin(username: String, password: String) {
        showLoading(true)

        lifecycleScope.launch {
            try {
                // Set API base URL before making request
                RetrofitClient.setBaseUrl(prefsManager.getApiBaseUrl())
                
                val apiService = RetrofitClient.getApiService()
                val response = apiService.login(username, password)

                if (response.isSuccessful && response.body() != null) {
                    val loginResponse = response.body()!!
                    
                    // Save authentication token and user info
                    prefsManager.saveAuthToken(loginResponse.accessToken)
                    prefsManager.saveUserInfo(
                        loginResponse.user.email,
                        loginResponse.user.fullName,
                        loginResponse.user.role
                    )

                    showToast("Login successful!")
                    
                    // Navigate to MainActivity
                    val intent = Intent(this@LoginActivity, com.esalama.gatescanner.MainActivity::class.java)
                    intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
                    startActivity(intent)
                    finish()
                } else {
                    showToast("Login failed: Invalid credentials")
                }
            } catch (e: Exception) {
                showToast("Login error: ${e.message}")
                e.printStackTrace()
            } finally {
                showLoading(false)
            }
        }
    }

    private fun showLoading(show: Boolean) {
        progressBar.visibility = if (show) View.VISIBLE else View.GONE
        loginButton.isEnabled = !show
        usernameEditText.isEnabled = !show
        passwordEditText.isEnabled = !show
    }

    private fun showToast(message: String) {
        runOnUiThread {
            Toast.makeText(this, message, Toast.LENGTH_LONG).show()
        }
    }
}
