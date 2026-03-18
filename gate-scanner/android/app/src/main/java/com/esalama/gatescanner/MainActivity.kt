package com.esalama.gatescanner

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.esalama.gatescanner.ui.LoginActivity
import com.esalama.gatescanner.ui.QRScannerActivity
import com.esalama.gatescanner.ui.SettingsActivity
import com.esalama.gatescanner.utils.PreferencesManager

/**
 * Main activity - Entry point of the app
 */
class MainActivity : AppCompatActivity() {

    private lateinit var prefsManager: PreferencesManager
    private lateinit var welcomeTextView: TextView
    private lateinit var scanButton: Button
    private lateinit var settingsButton: Button
    private lateinit var logoutButton: Button

    companion object {
        private const val CAMERA_PERMISSION_REQUEST_CODE = 100
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        prefsManager = PreferencesManager(this)

        // Check if user is logged in
        if (!prefsManager.isLoggedIn()) {
            navigateToLogin()
            return
        }

        // Initialize views
        welcomeTextView = findViewById(R.id.welcomeTextView)
        scanButton = findViewById(R.id.scanButton)
        settingsButton = findViewById(R.id.settingsButton)
        logoutButton = findViewById(R.id.logoutButton)

        // Set welcome message
        val userName = prefsManager.getUserName() ?: "User"
        welcomeTextView.text = "Welcome, $userName"

        // Set up button listeners
        scanButton.setOnClickListener {
            checkCameraPermissionAndStartScanner()
        }

        settingsButton.setOnClickListener {
            startActivity(Intent(this, SettingsActivity::class.java))
        }

        logoutButton.setOnClickListener {
            performLogout()
        }
    }

    private fun checkCameraPermissionAndStartScanner() {
        if (ContextCompat.checkSelfPermission(
                this,
                Manifest.permission.CAMERA
            ) == PackageManager.PERMISSION_GRANTED
        ) {
            startQRScanner()
        } else {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.CAMERA),
                CAMERA_PERMISSION_REQUEST_CODE
            )
        }
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == CAMERA_PERMISSION_REQUEST_CODE) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startQRScanner()
            } else {
                Toast.makeText(
                    this,
                    "Camera permission is required to scan QR codes",
                    Toast.LENGTH_LONG
                ).show()
            }
        }
    }

    private fun startQRScanner() {
        val intent = Intent(this, QRScannerActivity::class.java)
        startActivity(intent)
    }

    private fun performLogout() {
        prefsManager.clearAuth()
        navigateToLogin()
    }

    private fun navigateToLogin() {
        val intent = Intent(this, LoginActivity::class.java)
        intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
        startActivity(intent)
        finish()
    }
}
